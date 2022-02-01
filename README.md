# Books
Backend for on demand printig software.


Main features:
1. Browse all available products
2. User can select 1 or more available products and product can be added to the cart
3. Order will be placed for the items in the cart. 
4. Shipment of the books will be done by third paty. 

Overview:
The application is devided into Microservices. 
There are 2 services
1. BookStore - Provides the APIs where Books (available products) can be fetched from the database. 
   - Get all available books
   - Get book by id
   
2. BookPrinting - Provides the APIs for adding the books in the cart and place the order along with shipment details
   - Add books to the cart
   - Place the order for selected products in the cart. Once order is placed, the products will be removed from the cart.
   - Created sample methods for shipment tracking using 3rd party services.
   
  
Technology Stack:
Language - Python 3.7
REST API Framework - FastAPI
Database - MongoDB


