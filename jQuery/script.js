var data = [{"division":"�c�ƕ�","person":[{"name":'�R�c',"age":21},{"name":'����',"age":56},{"name":'���',"age":33}]},{"division":"������","person":[{"name":'����',"age":44},{"name":'����',"age":19},{"name":'�n��',"age":26}]}];

function json(){
    for(var i in data){
        $("#output").append("<li><strong>" + data[i].division + "</strong></li>");
        for(var j in data[i].person){
            $("#output").append("<lo>" + data[i].person[j].name + "�i" + data[i].person[j].age + "�ˁj</lo><br>");
        }
    }
}

$(function(){
    $(".hoge1").css("color","blue")
});

$(function(){
  $(".hoge2A").click(function(){
      $(this).css("background-color","green");
  })
});
  
$(function(){
  $(".hoge2B").click(function(){
      $(".hoge2B").toggle();
  });
});

$(function(){
  $(".hoge2C").click(function(){
      $(this).hide();
  });
});


function fadeOut(){
  $(".hoge2D").fadeOut(20000);
}

$(function() {
   $("#tbl2 tr:odd td").css('background', 'rgb(198, 226, 255)');
});

$(function() {
  $('#navi > h4').click(function(){
      $(this).next().slideToggle(100);
  });
});

$("#animate").click(function(){
  $(".block").animate(
    {width: "toggle", opacity: "toggle"},
    {duration: "slow", easing: "linear",
     complete: function(){alert("completed!");},
     step: function(s){$("#steps").text(s)}
    }
  );
});