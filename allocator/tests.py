from django.test import TestCase, Client
from django.urls import reverse
from .models import Box, Product, Order, OrderItem

class BoxSelectionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('box_selector')

        # Create Boxes
        self.small_box = Box.objects.create(
            name="Small Box", length=10, width=10, height=10, 
            max_weight_capacity=5, cost=10.00
        ) # Volume: 1000, Max Dim: 10
        
        self.large_box = Box.objects.create(
            name="Large Box", length=30, width=30, height=30, 
            max_weight_capacity=20, cost=25.00
        ) # Volume: 27000, Max Dim: 30

        # Create Products
        self.mouse = Product.objects.create(
            name="Wireless Mouse", length=5, width=5, height=2, weight=0.2
        ) # Volume: 50, Max Dim: 5
        
        self.laptop = Product.objects.create(
            name="Laptop", length=25, width=15, height=2, weight=2.0
        ) # Volume: 750, Max Dim: 25

        self.tv = Product.objects.create(
            name="Big TV", length=100, width=50, height=10, weight=15.0
        ) # Volume: 50000, Max Dim: 100 (Too big for any box)

    def test_model_calculations(self):
        """Test that the @property methods calculate volume and dimensions correctly."""
        self.assertEqual(self.small_box.volume, 1000)
        self.assertEqual(self.small_box.max_dimension, 10)
        self.assertEqual(self.mouse.volume, 50)
        self.assertEqual(self.mouse.max_dimension, 5)

    def test_single_box_order(self):
        """Test an order that easily fits into a single small box."""
        response = self.client.post(self.url, {
            f'quantity_{self.mouse.id}': '2'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('order', response.context)
        self.assertEqual(len(response.context['shipments']), 1)
        self.assertEqual(response.context['shipments'][0]['box'].name, "Small Box")
        
        # Verify database creation
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)
        self.assertEqual(OrderItem.objects.first().quantity, 2)

    def test_split_box_order(self):
        """Test a large order that exceeds a single box and must be split."""
        # 12 laptops = 24kg total. Max box weight is 20kg.
        # This MUST split into at least two boxes.
        response = self.client.post(self.url, {
            f'quantity_{self.laptop.id}': '12'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('order', response.context)
        
        # Check that multiple shipments were created
        shipments = response.context['shipments']
        self.assertGreater(len(shipments), 1)
        
        # Verify the sum of shipped weights matches total order weight (24kg)
        total_shipped_weight = sum(s['weight'] for s in shipments)
        self.assertEqual(total_shipped_weight, 24.0)

    def test_oversized_item_rejection(self):
        """Test that an item larger than any available box returns an error."""
        response = self.client.post(self.url, {
            f'quantity_{self.tv.id}': '1'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)
        self.assertNotIn('order', response.context)
        self.assertIn("too large or heavy", response.context['error'])

    def test_empty_submission(self):
        """Test submitting the form with 0 quantities."""
        response = self.client.post(self.url, {
            f'quantity_{self.mouse.id}': '0',
            f'quantity_{self.laptop.id}': '0'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)
        self.assertEqual(response.context['error'], "Please select at least one product.")