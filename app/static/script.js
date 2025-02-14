
// Scripts for home.html (__init__.py's function home() and submit_ratings()
function generateRatingFields() {
    console.log("entered generateRatingFields")
    const numRatings = document.getElementById("num_ratings")
    const ratingContainer = document.getElementById("rating_container")
    console.log(anime_list)
    const numRatingsValue = parseInt(numRatings.value, 10)

    console.log(numRatings.innerHTML);
    console.log(ratingContainer.innerHTML);
    // Reset the ratingContainer -- incase there were prior selections
    ratingContainer.innerHTML = '';


    for (let i = 1; i < numRatingsValue; i++) {
        let div = document.createElement('div')
        div.innerHTML = `
        <label for="rating_id${i}">Anime ${i} Rating (1-10):</label>
        <select name="rating_id${i}" id="rating_id${i}">
        ${Array.from({length: 19}, (_, j) => {
            const value = (j + 2) / 2; // generate from 1.0 - 10.0
            return `<option value="${value}">${value}</option>`;
        }).join('')}
        </select>
       
        `;
        ratingContainer.appendChild(div);

    }
    console.log("finish")
}

function submitRatings(){

}
window.onload = function() {
    console.log("Page loaded"); // Debugging: Confirm the page is loaded
    generateRatingFields(); // Generate fields based on the default selected value
};
