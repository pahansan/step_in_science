import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.table import Table

# Чтение данных
df = pd.read_csv('text_table/combined_speedup_table.txt', delim_whitespace=True)
df.set_index('Loop', inplace=True)
df = df.transpose()  # Транспонируем для удобства отображения

def fix_text(text):
    if isinstance(text, str):
        return text.replace('_', ' ')
    return text

def value_to_color(value):
    """Цвет по числу: <1 красный, =1 жёлтый, >1 зелёный, лог-контраст"""
    try:
        val = float(value)
    except:
        return '#FFFFFF'

    # Параметр лог-контраста: чем больше exponent, тем быстрее насыщается цвет
    exponent = 0.3

    if val == 1:
        return '#fed98e'  # жёлтый
    elif val < 1:
        # Красный градиент (<1): применяем log для усиления
        norm_val = 1 - val  # 0 → желтый, 1 → красный
        adjusted = norm_val**exponent
        return mcolors.to_hex(mcolors.LinearSegmentedColormap.from_list("", ["#fed98e","#fc8d59"])(adjusted))
    else:
        # Зеленый градиент (>1): лог-контраст
        max_val = df.to_numpy().max()
        norm_val = (val - 1) / (max_val - 1)  # 0 → желтый, 1 → зеленый
        adjusted = norm_val**exponent
        return mcolors.to_hex(mcolors.LinearSegmentedColormap.from_list("", ["#fed98e","#78c679"])(adjusted))

def create_table_image(data_subset, output_filename):
    n_data_rows, n_data_cols = data_subset.shape

    first_col_width = 1.4
    data_cell_size = 0.3
    header_height = 0.6

    total_width = first_col_width + n_data_cols * data_cell_size
    total_height = header_height + n_data_rows * data_cell_size

    col_widths = [first_col_width/total_width] + [data_cell_size/total_width] * n_data_cols
    row_heights = [header_height/total_height] + [data_cell_size/total_height] * n_data_rows

    col_lefts = [0]
    for w in col_widths[:-1]:
        col_lefts.append(col_lefts[-1] + w)

    row_bottoms = []
    cumulative = 0
    for h in row_heights[::-1]:
        row_bottoms.append(cumulative)
        cumulative += h
    row_bottoms = row_bottoms[::-1]

    fig, ax = plt.subplots(figsize=(total_width * 2, total_height * 2))
    ax.axis('off')
    table = Table(ax, bbox=[0, 0, 1, 1])
    table.auto_set_font_size(False)
    font_size = 14

    # Пустая ячейка в левом верхнем углу
    cell = table.add_cell(0, 0, col_widths[0], row_heights[0], text='', facecolor='white')
    cell.set_text_props(fontsize=font_size)
    cell.xy = (col_lefts[0], row_bottoms[0])

    # Заголовки столбцов
    for j, col_name in enumerate(data_subset.columns, start=1):
        cell = table.add_cell(
            0, j,
            col_widths[j], row_heights[0],
            text=fix_text(col_name),
            facecolor='white', loc='center'
        )
        cell.get_text().set_fontsize(font_size)
        cell.get_text().set_rotation(90)
        cell.get_text().set_verticalalignment('center')
        cell.xy = (col_lefts[j], row_bottoms[0])

    # Метки строк
    for i, row_label in enumerate(data_subset.index, start=1):
        cell = table.add_cell(
            i, 0,
            col_widths[0], row_heights[i],
            text=fix_text(row_label),
            facecolor='white', loc='center'
        )
        cell.get_text().set_fontsize(font_size)
        cell.xy = (col_lefts[0], row_bottoms[i])

    # Заполнение ячеек данными с окраской
    for i in range(n_data_rows):
        for j in range(n_data_cols):
            value = round(data_subset.iloc[i, j], 1)
            color = value_to_color(value)
            cell = table.add_cell(
                i+1, j+1,
                col_widths[j+1], row_heights[i+1],
                text=fix_text(value),
                facecolor=color, loc='center'
            )
            cell.get_text().set_fontsize(font_size)
            cell.xy = (col_lefts[j+1], row_bottoms[i+1])

    ax.add_table(table)
    plt.savefig(output_filename, bbox_inches='tight', dpi=300)
    plt.close()

cols_per_image = 31
num_chunks = len(df.columns) // cols_per_image + (1 if len(df.columns) % cols_per_image else 0)

for i in range(num_chunks):
    start_idx = i * cols_per_image
    end_idx = min((i + 1) * cols_per_image, len(df.columns))
    data_chunk = df.iloc[:, start_idx:end_idx]

    output_filename = f'png_table/table_part_{i + 1}.png'
    create_table_image(data_chunk, output_filename)
    print(f'Saved {output_filename}')

print("All tables have been generated.")
