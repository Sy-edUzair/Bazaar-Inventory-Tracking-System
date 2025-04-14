# Bazaar Inventory System

A comprehensive inventory management system built with Django REST Framework for tracking products, stores, stock levels, and movements across multiple retail locations.

## Features

- Product catalog management with SKU tracking
- Multi-store inventory tracking
- Stock movement recording (stock in, sales, manual removals)
- Detailed audit logging for all system actions
- RESTful API with comprehensive filtering
- Interactive API documentation with Swagger/Redoc

## Technology Stack

- Django 5.1.7
- Django REST Framework 3.16.0
- POSTGreSQL
- Swagger/Redoc Documentation

## Design Decisions

Implemented an MVC architecture by dividing functions into different modules for easier debugging and considering the system needs to be horizontally scalable in later version, this architecture suits it much better as it grants greater flexibility for updates.

## System Architecture

The system follows a modular (MVC) architecture with the following components:

- **inventory app**: Core data models
- **api app**: REST API endpoints and serializers
- **Django Admin**: Administrative interface

## Models

### Product
Represents items in the inventory system:
- UUID primary key
- SKU (unique identifier)
- Name, description
- Unit price
- Creation/update timestamps

### Store
Represents physical or virtual retail locations:
- UUID primary key
- Name, location
- Contact information
- Active status flag
- Creation/update timestamps

### Inventory
Links products to stores with quantity tracking:
- UUID primary key
- Store and product foreign keys
- Current quantity
- Last updated timestamp

### StockMovement
Records all changes to inventory levels:
- UUID primary key
- Store and product references
- Movement type (STOCK_IN, SALE, MANUAL_REMOVAL)
- Quantity
- Reference number and notes
- Timestamp

### AuditLog
Maintains a comprehensive record of all system activities:
- UUID primary key
- Action type and entity information
- User information
- JSON details for flexible logging
- IP address and timestamp

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/products/` | Product management |
| `/stores/` | Store management |
| `/inventory/` | Inventory level management |
| `/inventory/by_store/` | Inventory filtered by store |
| `/stock-movements/` | Stock movement operations |
| `/audit-logs/` | System activity logs |
| `/swagger/` | Interactive API documentation |
| `/redoc/` | Alternative API documentation |

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/bazaar-inventory.git
cd bazaar-inventory
```

2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up POSTGreSQL database:
   - Create a database named "Inventory System"

5. Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser
```bash
python manage.py createsuperuser
```

7. Run the development server
```bash
python manage.py runserver
```

8. Access the admin interface at http://127.0.0.1:8000/admin/
9. Access API documentation at http://127.0.0.1:8000/swagger/
OR
10. Login as admin
11. Access http://127.0.0.1:8000/ to have a built in API interface for testing and entering data

## Evolution Rationale (v1->v3)

### V1 goals achieved:
- Created a Model for product , stock movements, inventory.
- Implemented a Simple CLI interface
- Stored data locally in SQLite file

### V2 goals achieved:
- Added REST APIs for different models
- Enable filtering by stores through API
- Used a Relational DB (PostGreSQL)
- Introduced Basic Auth (Through Admin Panel)

### V3 goals achieved:
- Only implemented Audit logs from this because of time constraint

### V3 vision:
- Event-driven architecture using Kafka or Celery for background tasks
- Automated stock movements integrated with POS systems
- Real-time inventory updates
- Seperate Read/Write operations (Can be done through Routing with SQLAlchemy)

## Security Notes

- Replace the default Django secret key in production
- Disable debug mode in production environments
- Configure proper authentication for production use
- Set up proper database credentials
- Implement HTTPS in production

## Contact

For support or inquiries, contact: usyed249@gmail.com / https://www.linkedin.com/in/syed-uzair-hussain/
