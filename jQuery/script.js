var data = [{"division":"�c�ƕ�","person":[{"name":'�R�c',"age":21},{"name":'����',"age":56},{"name":'���',"age":33}]},{"division":"������","person":[{"name":'����',"age":44},{"name":'����',"age":19},{"name":'�n��',"age":26}]}];

function json(){
    for(var i in data){
        $("#output").append("<li><strong>" + data[i].division + "</strong></li>");
        for(var j in data[i].person){
            $("#output").append("<lo>" + data[i].person[j].name + "�i" + data[i].person[j].age + "�ˁj</lo><br>");
        }
    }
}