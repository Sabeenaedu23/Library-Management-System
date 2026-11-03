const bookForm = document.getElementById("bookForm");

bookForm.addEventListener("submit", function (event) {

    const title = bookForm.querySelector(
        'input[name="title"]'
    ).value.trim();

    const author = bookForm.querySelector(
        'input[name="author"]'
    ).value.trim();

    if (title === "" || author === "") {
        event.preventDefault();
        alert("Please enter both book title and author.");
    }

});