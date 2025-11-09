import sys

def read_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    data = []
    for line in lines[1:]:  # пропускаем заголовок
        parts = line.split()
        if len(parts) >= 2:
            try:
                col1 = parts[0]
                col2 = float(parts[1])
                data.append((col1, col2))
            except ValueError:
                continue
    return data

def main(file1, file2, output_file):
    data1 = read_file(file1)
    data2 = read_file(file2)
    
    if len(data1) != len(data2):
        print("Warning: Files have different number of data rows!")
        # Будем обрабатывать только строки, которые есть в обоих файлах
        min_len = min(len(data1), len(data2))
        data1 = data1[:min_len]
        data2 = data2[:min_len]
    
    results = []
    for (col1_1, val1), (col1_2, val2) in zip(data1, data2):
        if col1_1 != col1_2:
            print(f"Warning: Mismatch in first column: '{col1_1}' vs '{col1_2}'")
        if val2 == 0:
            speedup = float('inf')
        else:
            speedup = round(val1 / val2, 2)
        results.append((col1_1, speedup))
    
    with open(output_file, 'w') as f:
        f.write("Loop\tSpeedup\n")
        for col1, speedup in results:
            f.write(f"{col1}\t{speedup}\n")
    
    print(f"Results written to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <file1> <file2> <output_file>")
        sys.exit(1)
    
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    output_file = sys.argv[3]
    
    main(file1, file2, output_file)