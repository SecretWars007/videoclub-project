import os 
import sys 
from datetime import datetime 
# Asegurar que el directorio app esté en el path 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) 
from app.core.database import get_db_client 
from app.repositories.video_repository import VideoRepository 
from app.repositories.copy_repository import CopyRepository
from app.repositories.client_repository import ClientRepository 

def seed_database(): 
    client = get_db_client() 
    print("🌱 Iniciando poblamiento de datos iniciales en OpenSearch...") 
    video_repo = VideoRepository(client=client) 
    copy_repo = CopyRepository(client=client) 
    client_repo = ClientRepository(client=client) 
    # 1\. Poblar Películas 
    videos_data = [ 
        { 
            "video_id": "vid\_001", 
            "title": "Inception", 
            "alternative_titles": ["Origen", "El Origen"], "genre": "Sci-Fi", 
            "release_year": 2010, 
            "duration_minutes": 148, 
            "actors": ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Elliot Page"], 
            "oscar_info": [{"category": "Best Cinematography", "year": 2011, "won": True}], "dvd_unit_cost_bs": 35.0, "total_copies_acquired": 3 
        }, 
        { 
            "video_id": "vid_002", 
            "title": "The Godfather", "alternative_titles": ["El Padrino"], 
            "genre": "Drama", 
            "release_year": 1972, 
            "duration_minutes": 175, "actors": ["Marlon Brando", "Al Pacino", "James Caan"], "oscar_info": [{"category": "Best Picture", "year": 1973, "won": True}], "dvd_unit_cost_bs": 40.0, "total_copies_acquired": 2 
        }, 
        { 
            "video_id": "vid_003", 
            "title": "Interstellar", 
            "alternative_titles": ["Interestelar"], "genre": "Sci-Fi", 
            "release_year": 2014, 
            "duration_minutes": 169, 
            "actors": ["Matthew McConaughey", "Anne Hathaway", "Jessica Chastain"], 
            "oscar_info": [{"category": "Best Visual Effects", "year": 2015, "won": True}], "dvd_unit_cost_bs": 38.0, "total_copies_acquired": 2 
        } 
    ] 
    for v in videos_data: 
        v_id = v.pop("video_id") 
        v["created\_at"] = datetime.utcnow().isoformat()
        video_repo.index_document(v_id, v) 
        print(f" 🎬 Película indexada: {v['title']} ({v_id})")
    # 2. Poblar Copias Físicas 
    copies_data = [ 
        {"copy_id": "cop_101", "video_id": "vid_001", "video_title": "Inception", "status": "available", "condition": "excellent"}, 
        {"copy_id": "cop_102", "video_id": "vid_001", "video_title": "Inception", "status": "available", "condition": "good"}, 
        {"copy_id": "cop_103", "video_id": "vid_001", "video_title": "Inception", "status": "rented", "condition": "good"}, 
        {"copy_id": "cop_201", "video_id": "vid_002", "video_title": "The Godfather", "status": "available", "condition": "good"}, 
        {"copy_id": "cop_301", "video_id": "vid_003", "video_title": "Interstellar", "status": "available", "condition": "excellent"} 
    ] 
    for c in copies_data: 
        c_id = c.pop("copy_id") 
        c["updated_at"] = datetime.utcnow().isoformat()
        copy_repo.index_document(c_id, c)
        print(f" 📀 Copia indexada: {c['video_title']} - ID: {c_id} ({c['status']})") 
    # 3\. Poblar Clientes (Coordenadas en Bolivia) 
    clients_data = [ 
        { 
            "client_id": "cli_001", 
            "full_name": "Carlos Mamani", 
            "ci_nit": "6849301", 
            "phone": "71234567", 
            "email": "carlos.mamani@email.com", 
            "location": {"lat": -16.5000, "lon": -68.1500}, # La Paz Centro 
            "address_description": "Av. 16 de Julio, El Prado", 
            "is_blocked": False 
        }, 
        { 
            "client_id": "cli_002", 
            "full_name": "Ana Gutierrez", 
            "ci_nit": "4920192", 
            "phone": "72987654", 
            "email": "ana.gutierrez@email.com", 
            "location": {"lat": -16.5100, "lon": -68.1200}, # Sopocachi, La Paz 
            "address_description": "Plaza Abaroa", 
            "is_blocked": False 
        }, 
        { 
            "client_id": "cli_003", 
            "full_name": "Roberto Vargas (Bloqueado)", 
            "ci_nit": "3910293", 
            "phone": "70112233", 
            "email": "roberto.vargas@email.com", 
            "location": {"lat": -17.3895, "lon": -66.1568}, # Cochabamba 
            "address_description": "Av. Heroínas", 
            "is_blocked": True 
        } 
    ] 
    for cl in clients_data: 
        cl_id = cl.pop("client_id") 
        cl["registered_at"] = datetime.utcnow().isoformat() 
        client_repo.index_document(cl_id, cl) 
        print(f" 👤 Cliente indexado: {cl['full_name']} ({cl_id})") 
    print("\n✅ ¡Poblamiento de datos completado exitosamente!") 
# funcion que permite poblar la base de datos con datos iniciales 
if __name__ == "__main__": 
    seed_database()