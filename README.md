# aiPizzaOrdering
a simple chatbot for pizza ordering instructions

Este proyecto esta hecho para comunicarse on un API, donde enviara la orden despues de la confirmacion.

Para hacerlo de modo "Hands-on Lab", voy a dejar la creacion de dicha API por fuera,
solamente voy a dar una pista: Puede utilizar una Inteligencia Artificial Generativa para que le asista en la generacion de dicha API:
ejemplo: 
con la siguiente instruccion, pida a la GenAI que genere el codigo para la API: 
Generate a php rest api using slim framework, the api receives a json payload for a pizza object with the following properties: orderid, ordertype, toppings object with topping name, and topping type.
The API should load a data.json file that contains an array of existing orders and append the new one to the array and save the array to the file again, if the file does not exists, it can create it.
Then the API can also display the existing orders from the file in an html table
