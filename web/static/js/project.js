/*    Copyright (C) 2021  The Project TONA Authors
*
*    This program is free software: you can redistribute it and/or modify
*    it under the terms of the GNU General Public License as published by
*    the Free Software Foundation, either version 3 of the License, or
*    (at your option) any later version.
*
*    This program is distributed in the hope that it will be useful,
*    but WITHOUT ANY WARRANTY; without even the implied warranty of
*    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*    GNU General Public License for more details.
*
*    You should have received a copy of the GNU General Public License
*    along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

(function(window){
    function TonaProject (){
        var self = {};
        self.Add = function (){
            var txtName = document.querySelector(".modal #project-name");
            if (txtName.value != ""){
                fetch("/api/project", {
                    method: 'post',
                    body: JSON.stringify({
                        "name": txtName.value,
                    }),
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    },
                }).then(response => response.json()).then(function(data){
                    console.log(data)
                    var project_menu_list = document.querySelector("#project-menu-list");
                    var li = document.createElement("li");
                    li.innerHTML = '<a><span class="icon"><i class="fas fa-tasks"></i></span>'+txtName.value+'</a>';
                    project_menu_list.append(li);
                    txtName.value = ""
                    Tona.Modal.Close()
                }).catch(function(error){
                    console.error(error);
                });
            }
        };

        /*Task*/
        self.AddTask = function (e){
            var txtName = document.querySelector("#task-name");
            var txtProjectId = document.querySelector("#project-id");
            if (e.keyCode == 13 && txtName.value != "" && txtProjectId.value != ""){
                fetch("/api/project/task", {
                    method: 'post',
                    body: JSON.stringify({
                        "project_id": txtProjectId.value,
                        "name": txtName.value,
                    }),
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    },
                }).then(response => response.json()).then(function(data){
                    console.log(data)
                    var todo_menu_list = document.querySelector("#todo-menu-list");
                    var li = document.createElement("li");
                    li.innerHTML = '<a><label class="checkbox"><input type="checkbox" class="mr-2">'+txtName.value+'</label></a>';
                    todo_menu_list.append(li);
                    txtName.value = ""
                }).catch(function(error){
                    console.error(error);
                });
                
            }            
        };

        self.EditTask = function(e, id, field, value=null){
            var data = {};
            if (e != null && value == null){
                data[field]= e.target.value;
            }else if (e != null && value != null){
                data[field]= value;
            }
            if (field == 'due') {
                var utc = new Date(new Date( data[field]).getTime());
                data[field]= utc.toISOString();
            }
            fetch("/api/project/task/"+id, {
                method: 'put',
                body: JSON.stringify(data),
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
            }).then(response => response.json()).then(function(data){
                console.log(data)
            }).catch(function(error){
                console.error(error);
            });
        }

        self.onDragStartTask = function (event){
            event
            .dataTransfer
            .setData('text/plain', event.target.parentNode.id);
            event
            .currentTarget.style.backgroundColor = 'yellow';
        }
        self.onDragOverTask = function (event) {
            event.preventDefault();
        }
        self.onDropTask = function (event) {
            var status = event.target.id.split('-')[0];
            if (status == 'todo' || status == 'doing' || status == 'review'){
                const id = event.dataTransfer.getData('text');
                const draggableElement = document.getElementById(id);
                const dropzone = event.target;          
                dropzone.nextElementSibling.appendChild(draggableElement)
                event.dataTransfer.clearData();
                var task_id =  parseInt(id.split('-')[3])
                if (task_id > 0){
                    self.EditTask(event, task_id, 'status', status)
                }
                    
            }
          }
        return self;
    }
    if (typeof(window.TonaProject) === 'undefined'){
        window.TonaProject = TonaProject();
    }
})(window);