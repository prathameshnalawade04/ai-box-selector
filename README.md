# AI-Assisted Box Selection System

A Django-based ecommerce warehouse tool that recommends the most cost-effective shipping box for an order based on item dimensions, volume, and weight. It includes a greedy algorithm to split large orders across multiple boxes when they exceed the capacity of a single box.

## Features
- Calculates volume and max dimensions for precise box fitting.
- Recommends the cheapest valid box.
- Splits large orders into multiple shipments automatically.
- Single-page Bootstrap 5 interface for placing test orders.
- Custom Django admin interface for managing Products and Boxes.

## Setup Instructions
1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install Django: `pip install django`
5. Run migrations: `python manage.py makemigrations` and `python manage.py migrate`
6. Create a superuser to add products and boxes: `python manage.py createsuperuser`
7. Run the development server: `python manage.py runserver`


## What Did I Learn in This Assignment?
I got to learn many technicial as well as logical stuff form the assignmet like relatioshgips between models and better way of using property decorator in the model by keeping the views clean and analysis the problem in middle and get to experiece the try and learn process



## Running Tests
Run the test suite to verify the box selection logic:
```bash
python manage.py test