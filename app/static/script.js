
// Scripts for home.html (__init__.py's function home() and submit_ratings()
function generateRatingFields() {
    console.log("entered generateRatingFields");
    const numRatings = document.getElementById("num_ratings");
    const ratingContainer = document.getElementById("rating_container");
    // from home.html: const anime_list = {{ names | tojson }}
    console.log(anime_list);
    const numRatingsValue = parseInt(numRatings.value, 10);

    console.log(numRatings.innerHTML);
    console.log(ratingContainer.innerHTML);
    // Reset the ratingContainer -- incase there were prior selections
    ratingContainer.innerHTML = '';


    for (let i = 1; i <= numRatingsValue; i++) {
        let div = document.createElement('div')
        div.innerHTML = `

        <label for="anime_js_id${i}">Anime ${i}:</label>
        <select name="anime_js_id${i}" id="anime_js_id${i}">
        ${Array.from({length: anime_list.name.length}, (_, k) => {
            const name = anime_list.name[k]; // this will create a list of anime names for the user to select
            const anime_json_id = anime_list.anime_id[k];
            return `<option value="${anime_json_id}">${name}</option>`;
        }).join('')}
        </select>
        
        <label for="rating_id${i}">Rating (1-10):</label>
        <select name="rating_id${i}" id="rating_id${i}">
        ${Array.from({length: 19}, (_, j) => {
            const value = (j + 2) / 2; // generate from 1.0 - 10.0
            return `<option value="${value}">${value}</option>`;
        }).join('')}
        </select>
       
        `;
        ratingContainer.appendChild(div);
    }
    console.log("finish");
}

function submitRatings(){
    const numRatings = document.getElementById("num_ratings");

    const numRatingsValue = parseInt(numRatings.value);

    const ratings = {};
    const ratingsArray = [];

    for (let i = 1; i <= numRatingsValue; i++){
        const ratingElement = document.getElementById(`rating_id${i}`);
        const rating = parseFloat(ratingElement.value);

        const selectedElement = document.getElementById(`anime_js_id${i}`);
        const selectedIndex = selectedElement.selectedIndex;
        const selectedOption = selectedElement.options[selectedIndex];
        const name = selectedOption.text

        const animeElement = document.getElementById(`anime_js_id${i}`);
        const animeJsonId = parseInt(animeElement.value);

        ratings[animeJsonId] = {'name' : name, 'rating' : rating};
        ratingsArray.push({ "anime_id" : animeJsonId, "name" : name, "rating" : rating});
    }
    console.log("Collected Ratings:", ratingsArray);
    fetch('/submit_ratings', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({"ratings": ratingsArray}),

    })
        .then(response => {
        console.log("Raw Response:", response);
        return response.text(); // Use .text() instead of .json() to inspect the raw response
         })
        .then(text => {
            console.log("Response Text:", text);
            try {
                const data = JSON.parse(text); // Manually parse the JSON
                console.log("Parsed JSON Data:", data);
            } catch (error) {
                console.error("Failed to parse JSON:", error);
            }
        })
        .catch(error => {
            console.error('Error', error)
            alert('An error occurred while submitting ratings.')
        })
        .then(text => {
            const data = JSON.parse(text)
            console.log(data)
            }
        );
    }
window.onload = function() {
    // Generate fields based on the default selected value
    generateRatingFields();
};
