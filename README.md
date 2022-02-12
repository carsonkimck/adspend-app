# adspend-app
Web application that helps users track their ad campaign spending across various platforms. Application is developed through Flask, a lightweight micro web framework written in Python. 


Flow:

Button to request Etsy authorization: link is generated, user clicks on link. Enables permission, redirects to site home page with etsy_code as url query parameter. Code is retrieved, 
used to retrieve an access token. Permanent access token is stored in database.

Etsy charges (resources) are called every time sheet is generated, charges should update for that month.

Google Flow:

Google link is generated on site button. Asks for sheets as well as adwords scope access. After authorization is accepted, it generates a access and refresh token for the user. 


When sheet is first initialized, it duplicates a template stored on the server (carsonkimck2001@gmail.com's Google drive) and sets the values to 0. It then prepares to update the charges for that month
by pulling first the Etsy charges and then the Google charges and setting their associated cells to that value. Whenever the sheet is generated, it will always call the API to generate the most 
updated numbers within that month - guaranteed. 



