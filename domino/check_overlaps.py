import xml.etree.ElementTree as ET
import numpy as np
import sys

def rotation_matrix(euler):
    rx, ry, rz = euler
    Rx = np.array([[1,0,0],[0,np.cos(rx),-np.sin(rx)],[0,np.sin(rx),np.cos(rx)]])
    Ry = np.array([[np.cos(ry),0,np.sin(ry)],[0,1,0],[-np.sin(ry),0,np.cos(ry)]])
    Rz = np.array([[np.cos(rz),-np.sin(rz),0],[np.sin(rz),np.cos(rz),0],[0,0,1]])
    return Rz @ Ry @ Rx

def load_xml(path):
    tree = ET.parse(path)
    root = tree.getroot()
    bodies = root.findall('.//body')
    data = []
    for b in bodies:
        pos = np.array(list(map(float, b.get('pos').split())))
        euler = np.array(list(map(float, b.get('euler', '0 0 0').split()))) * np.pi / 180
        geom = b.find('geom')
        size = np.array(list(map(float, geom.get('size').split())))
        data.append({'pos': pos, 'euler': euler, 'size': size, 'R': rotation_matrix(euler)})
    return data

def penetration(a, b):
    axes = []
    for i in range(3):
        axes.append(a['R'][:, i])
        axes.append(b['R'][:, i])
    for i in range(3):
        for j in range(3):
            ax = np.cross(a['R'][:, i], b['R'][:, j])
            if np.linalg.norm(ax) > 1e-8:
                axes.append(ax / np.linalg.norm(ax))
    min_pen = float('inf')
    for ax in axes:
        t = np.dot(b['pos'] - a['pos'], ax)
        ra = sum(a['size'][k] * abs(np.dot(a['R'][:, k], ax)) for k in range(3))
        rb = sum(b['size'][k] * abs(np.dot(b['R'][:, k], ax)) for k in range(3))
        pen = ra + rb - abs(t)
        if pen < min_pen:
            min_pen = pen
    return min_pen

def check_file(path):
    data = load_xml(path)
    overlaps = 0
    max_pen = 0
    for i in range(len(data)):
        for j in range(i+1, len(data)):
            pen = penetration(data[i], data[j])
            if pen > 1e-3:
                overlaps += 1
                if pen > max_pen:
                    max_pen = pen
    print(f"{path}: {len(data)} bodies, {overlaps} real overlaps (max_pen={max_pen:.4f})")
    return overlaps == 0

if __name__ == "__main__":
    ok = True
    for p in sys.argv[1:]:
        ok = check_file(p) and ok
    sys.exit(0 if ok else 1)
