from rdflib import Graph
import os

def test_connection():
    ttl_path = os.path.join("knowledge", "PotatoDisease.ttl")
    g = Graph()
    try:
        g.parse(ttl_path, format="turtle")
    except Exception as e:
        print("Gagal membaca file Turtle")
        print("Error:", e)
        return

    print("Berhasil membaca file Turtle")
    print("Total triple:", len(g))

    count = 0
    for s, p, o in g:
        print(s, p, o)
        count += 1
        if count == 5:
            break

if __name__ == "__main__":
    test_connection()
