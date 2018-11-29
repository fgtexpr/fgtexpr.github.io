from browser import document, alert

# bind event 'click' on button to function echo

def echo(ev):
    alert(document["zone"].value)
    document["mybutton"].bind("click", echo)
