window.addEventListener("DOMContentLoaded", function() {


    document.getElementById('characterSubmit').addEventListener('click', function () {
        postData('/api/editCharacter/' + 1 + '/', JSON.stringify())
          .then(data => {
            console.log("Posted to the server"); // JSON data parsed by `data.json()` call
          });
      });
});

async function postData(url = '', data = {}) {
    // Default options are marked with *
    const response = await fetch(url, {
      method: 'PUT',
      cache: 'no-cache',
      headers: {
        'Content-Type': 'application/json'
      },
      referrerPolicy: 'no-referrer', 
      body: data 
    });
    return await response.json(); // parses JSON response into native JavaScript objects
    }