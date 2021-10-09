## User Interfaces

https://cs50.harvard.edu/web/2020/notes/6/

---

### SPA - single page application

- instead of using different routes in our Django application, we have the ability to load just a single page and then use JavaScript to manipulate the DOM
- one major advantage of doing this is that we only need to modify the part of the page that is actually changing
- for example, if we have a Nav Bar that doesn’t change based on your current page, we wouldn’t want to have to re-render that Nav Bar every time we switch to a new part of the page