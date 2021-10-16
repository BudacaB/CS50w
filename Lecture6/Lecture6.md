## User Interfaces

https://cs50.harvard.edu/web/2020/notes/6/

---

### SPA - single page application

- instead of using different routes in our Django application, we have the ability to load just a single page and then use JavaScript to manipulate the DOM
- one major advantage of doing this is that we only need to modify the part of the page that is actually changing
- for example, if we have a Nav Bar that doesn’t change based on your current page, we wouldn’t want to have to re-render that Nav Bar every time we switch to a new part of the page

---

### JavaScript window object 

- represents the physical window on the PC screen
- certain properties of this object allow us to use some interesting features
- the document is the whole webpage - the windows is only the section displayed on the screen at any given time, the 'physical' part
- some properties:
    - window.innerWidth - how wide is the window - the px size of the user screen
    - window.innerHeight - height of the window
    - window.scrollY - how many px far down have you scrolled - e.g. 0 px at the top of the page, increasing as you scroll
    - document.body.offsetHeight - entire height of the page / document