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
    function Objective (){
        var self = {};
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        };
        self.AddObjective = function (e){
            var $modal = document.querySelector("#modal-add-objective");
            var name = $modal.querySelector("#objetive-name");
            var start = $modal.querySelector("#objetive-start");
            var due = $modal.querySelector("#objetive-due");

            if (name.value != "" && start.value != "" && due.value != ""){
                var data = {name: name.value, start: start.value, due: due.value};
                fetch("/api/objective", {
                    method: 'post',
                    body: JSON.stringify(data),
                    headers: self.headers,
                }).then(response => response.json()).then(function(data){
                    console.log(data);
                    var menu = document.querySelector("#objective-menu-list");
                    var li = document.createElement("li");
                    var objective = data['payload'];
                    li.innerHTML = '<a href="/objective/'+objective['id']+'">'+objective['name']+'</a>';
                    menu.append(li);
                    Tona.Modal.Close()
                    name.value = ""
                    start.value = ""
                    due.value = ""
                }).catch(function(error){
                    console.error(error);
                });
                
            }            
        };

        self.AddKeyResult = function (e){
            var name = e.target;
            if (e.keyCode == 13 && name.value != "" ){
                var data = {
                    name: name.value, 
                    objective_id:  name.dataset.objectiveId,
                    start: name.dataset.objectiveStart,
                    due: name.dataset.objectiveDue
                }
                fetch("/api/objective/keyresult", {
                    method: 'post',
                    body: JSON.stringify(data),
                    headers: self.headers,
                }).then(response => response.json()).then(function(data){
                    console.log(data)
                    var menu = document.querySelector("#objective-key-menu-list");
                    var li = document.createElement("li");
                    var payload = data['payload'];
                    li.innerHTML = '<a href="/objective/'+payload['objective_id']['id']+'/keyresult/'+payload['id']+'">'+payload['name']+'</a>';
                    menu.append(li);
                    name.value = ""
                }).catch(function(error){
                    console.error(error);
                });
                
            }
        };

        self.EditKeyResult = function(e, id, field, value=null){
            var data = {};
            if (e != null && value == null){
                data[field]= e.target.value;
            }else if (e != null && value != null){
                data[field]= value;
            }
            fetch("/api/objective/keyresult/"+id, {
                method: 'put',
                body: JSON.stringify(data),
                headers: self.headers,
            }).then(response => response.json()).then(function(data){
                console.log(data)
            }).catch(function(error){
                console.error(error);
            });
        }
        return self;
    }
    if (typeof(window.Objective) === 'undefined'){
        window.Objective = Objective();
    }
})(window);