User has to log in, that's how we remember who people are, then they're issued a token and remembered.
It's important to remember users when they navigate back to the page 
It would also be cool to remember a user and then show them their stats, vs everyone elses of the day. Would be pretty simple, just 
store how many steps it took for the daily entry. -- next steps.
-- Ideally we just simply do this via cookies. Am going to need to figure out how cookies work, can't be too hard. 

some designs:
1) 
When the user comes to the page, all the relevant game logic goes from there 
They come to the page, we get a token from them, then we issue all pertinant data. 
Then the front end does all of the business logic.
The problem with this though is that if a user navigates away from the page, then they have to retry all over again
It doesn't remember who you are. 

2) 
When the user comes to the page, they get all of the pertinent data -- (last guesses) and those are loaded into the front end,
each guess is sent to the backend, then the backend replies with how correct the guess was. 


Ideally, we actually would issue 
We then expose an API inorder 


