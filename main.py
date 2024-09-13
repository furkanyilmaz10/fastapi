import json
from fastapi import FastAPI, HTTPException, status

app = FastAPI()

# Path sabitlerini tanımlama
ITEMS_PATH = "/items"
ITEM_PATH = "/items/{item_id}"

# Veriyi saklamak için dosya text
DATA_FILE = "items.txt"

# Dosyadan veriyi yüklemek için    fonksiyon
def load_items():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}  # Eğer dosya yoksa boş bir sözlük yaz

# Dosyaya veriyi yazmak icinn fonksiyon
def save_items(items):
    with open(DATA_FILE, "w") as file:
        json.dump(items, file, indent=4)


# Uygulama başlangıcında datayı yüklemek için -->
items = load_items()

# 1. Tüm öğeleri listeleme
@app.get(ITEMS_PATH)
def get_items():
    return items

# 2. Belirtilen id'ye sahip öğeyi gösterme
@app.get(ITEM_PATH)
def get_item(item_id: int):
    if str(item_id) in items:
        return items[str(item_id)]
    else:
        raise HTTPException(status_code=404, detail="Requested item not found")

# 3. Yeni öğe ekleme (status 201 Created)
@app.post(ITEMS_PATH, status_code=status.HTTP_201_CREATED)
def create_item(item_id: int, name: str, description: str|None = None):
    if str(item_id) in items:
        raise HTTPException(status_code=400, detail="Item already exists, use PUT to update")
    items[str(item_id)] = {"name": name, "description": description}
    save_items(items)
    return items[str(item_id)]

# 4. Mevcut öğeyi güncelle veya yoksa yeni ekleme yap
@app.put(ITEM_PATH)
def update_item(item_id: int, name: str, description: str):
    if str(item_id) not in items:
        raise HTTPException(status_code=404, detail="Item not found, cannot update")
    items[str(item_id)] = {"name": name, "description": description}
    save_items(items)
    return items[str(item_id)]

# 5. Belirtilen id'ye sahip öğeyi sil
@app.delete(ITEM_PATH)
def delete_item(item_id: int):
    if str(item_id) in items:
        del items[str(item_id)]
        save_items(items)
        return {"message": f"Item {item_id} deleted"}
    else:
        raise HTTPException(status_code=404, detail="Item not found, cannot delete")
