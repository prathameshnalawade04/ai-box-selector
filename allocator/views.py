from django.shortcuts import render
from django.utils.crypto import get_random_string
from .models import Product, Box, Order, OrderItem

def get_cheapest_box(items, all_boxes):
    """Helper function to find the cheapest box for a list of items."""
    if not items:
        return None
        
    total_weight = sum(item.weight for item in items)
    total_volume = sum(item.volume for item in items)
    max_dim = max(item.max_dimension for item in items)

    suitable_boxes = [
        box for box in all_boxes 
        if box.max_weight_capacity >= total_weight 
        and box.volume >= total_volume 
        and box.max_dimension >= max_dim
    ]

    if suitable_boxes:
        # Sort by cost first, then volume
        suitable_boxes.sort(key=lambda b: (b.cost, b.volume))
        return suitable_boxes[0]
    return None

def create_order_and_find_box(request):
    products = Product.objects.all()
    context = {'products': products}

    if request.method == 'POST':
        flat_items = []
        
        # 1. Parse form and unroll quantities into a flat list
        for product in products:
            quantity_str = request.POST.get(f'quantity_{product.id}', '0')
            if quantity_str.isdigit() and int(quantity_str) > 0:
                for _ in range(int(quantity_str)):
                    flat_items.append(product)

        if not flat_items:
            context['error'] = "Please select at least one product."
            return render(request, 'box_selector.html', context)

        # Sort items by volume descending (largest first) to optimize packing
        flat_items.sort(key=lambda x: x.volume, reverse=True)
        all_boxes = list(Box.objects.all())

        # 2. Check if any single item is too big for the warehouse entirely
        for item in flat_items:
            if not get_cheapest_box([item], all_boxes):
                context['error'] = f"Item '{item.name}' is too large or heavy for any available box."
                return render(request, 'box_selector.html', context)

        # 3. Greedy packing logic
        shipments = []
        current_batch = []

        for item in flat_items:
            current_batch.append(item)
            # If the current batch doesn't fit in ANY box, the last item pushed it over the edge
            if not get_cheapest_box(current_batch, all_boxes):
                current_batch.pop()  # Remove the item that broke the limit
                
                # Assign the best box for the confirmed batch and save it
                assigned_box = get_cheapest_box(current_batch, all_boxes)
                shipments.append({
                    'box': assigned_box,
                    'items': current_batch,
                    'weight': sum(p.weight for p in current_batch),
                    'volume': sum(p.volume for p in current_batch),
                })
                
                # Start a new batch with the item we removed
                current_batch = [item]

        # 4. Process the final batch
        if current_batch:
            assigned_box = get_cheapest_box(current_batch, all_boxes)
            shipments.append({
                'box': assigned_box,
                'items': current_batch,
                'weight': sum(p.weight for p in current_batch),
                'volume': sum(p.volume for p in current_batch),
            })

        # 5. Save the Order to the database
        order_number = get_random_string(10).upper()
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            order_number=order_number
        )

        # Group flat items back into quantities for database saving
        item_counts = {}
        for item in flat_items:
            item_counts[item] = item_counts.get(item, 0) + 1
            
        for prod, qty in item_counts.items():
            OrderItem.objects.create(order=order, product=prod, quantity=qty)

        # 6. Calculate total order cost
        total_shipping_cost = sum(shipment['box'].cost for shipment in shipments)

        context.update({
            'order': order,
            'shipments': shipments,
            'total_shipping_cost': total_shipping_cost,
            'total_order_weight': order.total_weight,
        })

    return render(request, 'box_selector.html', context)