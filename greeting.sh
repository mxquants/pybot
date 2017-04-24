curl -X POST -H "Content-Type: application/json" -d '{
  "greeting":[
    {
      "locale":"default",
      "text":"Hi there!\n\nMy name is pyBot, the only bot that can talk with snakes! Use #py at the beginning of your code so I can speak Parseltongue with you!"
    }
  ] 
}' "https://graph.facebook.com/v2.6/me/messenger_profile?access_token=EAAaiAN9H6KEBANNiZCZA1xnwt1wxd9twtZADhHkfvpWHCh8JaVd7CNZB61Yb0jMZA4KAFChAyDNz74ZCpoaWyvNGH2khu6N8LdVEzePFJZC6ueCfvM9Tm9R0d8Ebj4DoZC8CTNbrVISI3DB0MMZBFtNQRlvH9WRcc2xfhS1tCTNJyOQZDZD"
