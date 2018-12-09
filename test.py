from browser import document, alert

# bind event 'click' on button to function echo

def echo(ev):
    alert("hello")

document["mybutton"].bind("click", echo)
