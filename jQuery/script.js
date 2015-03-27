var data = [{"division":"営業部","person":[{"name":'山田',"age":21},{"name":'佐藤',"age":56},{"name":'鈴木',"age":33}]},{"division":"製造部","person":[{"name":'阿部',"age":44},{"name":'藤沢',"age":19},{"name":'渡辺',"age":26}]}];

function json(){
    for(var i in data){
        $("#output").append("<li><strong>" + data[i].division + "</strong></li>");
        for(var j in data[i].person){
            $("#output").append("<lo>" + data[i].person[j].name + "（" + data[i].person[j].age + "才）</lo><br>");
        }
    }
}