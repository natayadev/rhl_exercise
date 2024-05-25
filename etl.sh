#!/bin/bash

# Directorios de entrada y salida
RAW_DIR="raw_data"
PROCESSED_DIR="processed_data"

if [ ! -d "$RAW_DIR" ]; then
    echo "Directorio $RAW_DIR no existe."
    exit 1
fi

if [ ! -d "$PROCESSED_DIR" ]; then
    echo "Directorio $PROCESSED_DIR no existe. Creando..."
    mkdir -p "$PROCESSED_DIR"
fi

# Función para seleccionar columnas específicas de un archivo CSV
seleccionar_columnas() {
    local input_file="$1"
    local output_file="$2"
    # Usar awk para seleccionar las columnas importantes
    awk -F',' '{
        output = ""
        for (i = 1; i <= NF; i++) {
            if (i == 3 || i == 7 || i == 9) {
                if (output == "") {
                    output = $i
                } else {
                    output = output "," $i
                }
            }
        }
        print output
    }' "$input_file" > "$output_file"
}

# Iterar sobre cada archivo .txt en el directorio de raw_data
for file in "$RAW_DIR"/*.txt; do
    # Obtener el nombre base del archivo (sin la extensión)
    base_name=$(basename "$file" .txt)
    
    # Convertir el archivo .txt a .csv usando awk
    csv_file="$PROCESSED_DIR/$base_name.csv"
    awk '
    {
        # Iniciar una línea vacía
        line = $1
        # Concatenar cada campo separado por comas
        for (i = 2; i <= NF; i++) {
            line = line "," $i
        }
        # Imprimir la línea procesada
        print line
    }
    ' "$file" > "$csv_file"
    
    # Crear un archivo temporal para almacenar el resultado
    temp_csv_file="${csv_file%.csv}_temp.csv"
    
    # Llamar a la función para seleccionar las columnas importantes
    seleccionar_columnas "$csv_file" "$temp_csv_file"
    
    # Reemplazar el archivo original con el archivo modificado
    mv "$temp_csv_file" "$csv_file"

    rm "$file"
    
    echo "Procesado $file, guardado en $csv_file y solo columnas importantes mantenidas."
done

echo "Todos los archivos han sido procesados, modificados y eliminados de $RAW_DIR."
