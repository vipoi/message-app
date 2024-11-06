## Description

1. Skicka meddelande till en mottagare (till exempel identifierad med epostadress, telefonnummer, användarnamn eller liknande)
2. Hämta nya (sedan förra hämtningen) meddelanden till mottagare
3. Ta bort ett eller flera meddelanden för en mottagare
4. Hämta tidsordnade meddelanden till en mottagare enligt start och stopp
index


## Data

Models:

User
* identifier

Message
* sender
* receiver
* text

## Api
Third party package https://github.com/encode/django-rest-framework

Messaging
* Send a message to a user
  `POST /messages`
* Retrieve messages from a user
  `GET /messages?q=filter`
* Delete a specific message
  `DELETE /messages/:id`

