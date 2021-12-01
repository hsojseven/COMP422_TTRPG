window.addEventListener("DOMContentLoaded", function() {
	
	const editBtn = document.getElementById("editButton");
	editBtn.addEventListener("click", pre_fill_form);
    
});


// Fill character form fields with the previously saved details
function pre_fill_form()
{
    
    document.getElementById('').setAttribute('value', valueFromSQL);
}
