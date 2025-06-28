from src.extract_data import run_extract
from src.transform_data import run_transform
from src.load_data import run_load

def main():
    print("🚀 Iniciando pipeline ETL de imóveis...\n")

    print("📥 Etapa 1: Extração dos dados")
    run_extract()

    print("🔧 Etapa 2: Transformação dos dados")
    run_transform()

    print("📤 Etapa 3: Carga no banco de dados")
    run_load()

    print("\n✅ Pipeline finalizado com sucesso!")

if __name__ == "__main__":
    main()
