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
inventory and sales. When starting out I'll be using an in memory
storage placed in 'src/main.py' and passed in as dependancy injection.

Inventory - view, add, archive, edit
Sales - view

Products of same name can exist. They will be identified with their ID.

It's prefered that the IDs never change because when the product is archived
it still need to be able to be viewed.
