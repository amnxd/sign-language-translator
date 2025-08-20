import json

# Read the notebook file
with open('hand-gesture-recognition-mediapipe/keypoint_classification.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Find and replace the model_save_path line
for cell in notebook['cells']:
    if cell['cell_type'] == 'code':
        for i, line in enumerate(cell['source']):
            if 'model_save_path = ' in line and '.hdf5' in line:
                cell['source'][i] = line.replace('.hdf5', '.keras')
                print(f"Fixed line: {line.strip()} -> {cell['source'][i].strip()}")

# Write the fixed notebook back
with open('hand-gesture-recognition-mediapipe/keypoint_classification.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print("Notebook fixed successfully!")

