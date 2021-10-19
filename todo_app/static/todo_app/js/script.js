// document.getElementById("superpower").addEventListener("click", function (e) {
//     document.getElementById("superpower").innerHTML = "It worked";
// });

const todo_lists = document.querySelectorAll(".list-name");
const tasks_displayed = document.querySelectorAll('input[type="checkbox"]');
const tasks_to_delete = []; 

function value_exists(value, arr) {
    let status = false;
    for (let i = 0; i < arr.length; i++) {
        let current_item_in_arr = arr[i];
        if (value == current_item_in_arr) {
            status = true;
            return status;
        } 
    }
    return status;
}


[...todo_lists].forEach(function(todo_list) {
    todo_list.addEventListener('click', function(e) {
        let active = document.querySelector(".active-list");
        active.className = '';
        active.classList.add('list-name');
        // set new "active" list 
        e.target.classList.add("active-list");
    });
});

[...tasks_displayed].forEach(function(task) {
    task.addEventListener('click', function(e) {
        let name = e.target.getAttribute("name");
        let exists = value_exists(name, tasks_to_delete);
        if (!exists) {
            tasks_to_delete.push(name);
            // create a new hidden element
            let new_element = document.createElement("input");
            new_element.setAttribute('type', 'hidden');
            new_element.setAttribute('name', name);
            new_element.setAttribute('id', name);

            // select the correct form element
            let form = document.getElementById("deleting");
            form.appendChild(new_element);
        } else {
            let selected_index = tasks_to_delete.indexOf(name);
            tasks_to_delete.splice(selected_index, 1);

            let remove_this_element = document.getElementById(name);
            remove_this_element.remove();

            
        }
    
    });
});

