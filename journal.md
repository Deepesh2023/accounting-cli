# Printos accounting module

This is my first time building something complex like a full blown accounting module.
I have experience with simple CRUD apps and simple CLI apps. Everything looks overwhelming
at the moment. I have to learn to break things down as small as possible and work one piece 
at a time. 

For this project, I will start with a CLI tool so to get familiar with the thing am building.
I have very little experience with accounting in general. I will work with things that i know
and iterate on it. Make something terrible fast then look over it.

## Why need a accounting module

- A store would have products
- Anyone can buy products from the store
- The change in quantity of stock is reflected in the inventory
- The store owner can keep track of stock as well as profit
- The store will likely have vendors where they get the stocks
- Have to keep track of expense in terms of product buying for the store

## Task 1- Build a simple inventor tracker 

Any shop will have a means to track their stock. The owner will be able to 

- List all products
- Add a product
- archive a product 
- update like price or quantity
- Quick qnt edit

A product will have

- Name 
  Not empty 
  Used to represent a product the store is selling. The name
  is used to identify the product and used for searching. Can
  be edited by the user.
- Selling price 
  The price at which the product is sold. Must be never negative.
  Used to charge the customer, keep track of transactions, and 
  calculate profit and loss. Can be edited by the user.
- Quantity 
  Used to keep track of a product's stock. Used to notify the owner
  low stock alert and track stats like most sold products. Must be 
  greater than 0. Can be edited by the user.
- an ID
  Should be unique. Used to identify the product
  on the database. Read only.

## Product lifecycle

- A product is identified using it's ID
- Store owner creates new product with a selling price
  and quantity
- When a customer buys x amounts of the said product, the
  stock of the product is reflected by reducing x from the
  stock.
- A product can be archived if necessary.


Everything else builds on top of this.

## Inventory storage design

The program stores all the products and can be edited and viewed.
The products can only be edited from the inventory but viewed by
inventory and sales. I'm using JSON file persistence in 'src/inventory/repository.py' 
and passed in as dependancy injection.

Inventory - view, add, archive, edit
Sales - view

Products of same name can exist. They will be identified with their ID.

It's prefered that the IDs never change because when the product is archived
it still need to be able to be viewed.

## Editing a product

While on inventory menu, user have the option to edit a certain product. The
user can edit the name, selling price, and quantity. The product to be edited
is identified by the product' id. A confirmation will be asked before confirming
the edit. 
When on edit mode, user will be shown a summary of the product and the options available
to edit. Either select a field to edit or cancel the operation.

## Sale

User can record a sale. A selling item consist of

- id
- name
- selling price
- quantity 

A product selected from the inventory for selling is now a selling item. The selling_price
and quantity can be edited. 

When editing, the quantity cannot go below the available stock of the product in the inventory
and the selling price cannot be negative. If either constraint is violated, the user is shown a warning.
If all goes well the product is now officially a selling product and can move to a list of selling items

The list of selling items is what the user can view as a table when recording sale. Here the user can

- add to the list (selling item)
- remove a selling item
- update a selling item

If a selling item is added that's already present in the list and with the same selling price,
it just updates the quantity of that specific item.

At the end of the list, a summary is shown with total price and total number quantity.

User now have the option to confirm the sale. Once confirmed, the quantity change is
reflected in the corresponding items in the inventory and the sale is recorded. A
sale has

- id
- date
- items (selling items)
- customer name (optional)

### Business rules

- A sale must contain at least one sale item.

- Sale quantity must be greater than zero.

- Sale quantity cannot exceed available inventory.

- Sale items with the same product and same selling price are merged.

- Inventory is updated only after the sale is confirmed.

- A completed sale cannot be edited.

- Sale history preserves the selling price at the time of purchase.

### Workflow

1. picks an item from inventory for sale. If the quantity is not more
than the quantity of the item in inventory and selling price is not negative,
its added to the selling list

2. If there is atleast one item in the selling list, the user can confirm the sale.

3. Once confirmed the quantity is reflected across the inventory, specifically the
products being sold. Then the sale is recorded

4. The user is now shown a fresh table for sales for a fresh start.

