function add_comment(button) {
    let parent = button
    do {
        parent = parent.parentElement
    } while (parent.nodeName !== "FORM")

    let ajax = new XMLHttpRequest()
    ajax.onreadystatechange = function () {
        if (this.status === 201) {
            location.reload()
            return
        }
        else if (!(this.readyState === 4 && this.status === 200)) {
            return
        }
        parent.parentElement.innerHTML = this.responseText;

    }
    let formData = new FormData(parent)
    ajax.open("POST", ADD_COMMENT_URL, true)
    ajax.send(formData)
}
