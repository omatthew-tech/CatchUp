const allNames = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", /* add the rest of the names here */];
let names = [...allNames]; // Create a copy of allNames to work with

function getRandomName() {
    if (names.length === 0) {
        names = [...allNames]; // If all names have been used, reset the list
    }
    const randomIndex = Math.floor(Math.random() * names.length);
    const name = names[randomIndex];
    names.splice(randomIndex, 1); // Remove the chosen name from the list
    return name;
}

const heading = document.getElementById('name-heading');
heading.textContent = getRandomName();

function changeName() {
    heading.classList.remove('fade');
    void heading.offsetWidth; // Trigger a reflow to reset the animation
    heading.textContent = getRandomName();
    heading.classList.add('fade');
}

setInterval(changeName, 5000); // Change the name every 5 seconds
