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
if ( !Date.prototype.toISOString ) {
    ( function() {
  
        function pad(number) {
          var r = String(number);
          if ( r.length === 1 ) {
            r = '0' + r;
          }
          return r;
        }
    
        Date.prototype.toISOString = function() {
          return this.getUTCFullYear()
            + '-' + pad( this.getUTCMonth() + 1 )
            + '-' + pad( this.getUTCDate() )
            + 'T' + pad( this.getUTCHours() )
            + ':' + pad( this.getUTCMinutes() )
            + ':' + pad( this.getUTCSeconds() )
            + '.' + String( (this.getUTCMilliseconds()/1000).toFixed(3) ).slice( 2, 5 )
            + 'Z';
        };
    
      }() );
}

(function(window){
  function Tona (){
      var self = {};

      self.NotificationDelete = function(){
        (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
          const $notification = $delete.parentNode;
      
          $delete.addEventListener('click', () => {
            $notification.parentNode.removeChild($notification);
          });
        });
      }
      self.Modal = {
        modal : null,
        Done: ()=>{},
        Close: function (){
          self.Modal.modal.classList.remove('is-active');
          self.Modal.modal = null;
        },
        Show : function(id){
          self.Modal.modal = document.getElementById(id);
          self.Modal.modal.classList.add('is-active');
          
          (self.Modal.modal.querySelectorAll('.modal-card-head .delete') || []).forEach(($delete)=>{
            $delete.addEventListener('click', self.Modal.Close);
          });
          
          (self.Modal.modal.querySelectorAll('.modal-card-foot button:not(.is-success)') || []).forEach(($delete)=>{
            $delete.addEventListener('click', self.Modal.Close);
          });
          
          /*(self.Modal.modal.querySelectorAll('.modal-card-foot button.is-success') || []).forEach(($delete)=>{
            console.log($delete);
            $delete.addEventListener('click', self.Modal.Done);
          });*/

        }, 

      };
      return self;
  }

  if (typeof(window.Tona) === 'undefined'){
    window.Tona = Tona();
  }
})(window);
