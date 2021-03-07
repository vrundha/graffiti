function my_func(e) {
  // e.preventDefault();
  e.stopPropagation();
  $('#post_on_wall').prop('disabled', true);
   $.post("/graffiti",
   {
     emo: document.getElementById('emotion').value,
     comm: document.getElementById('user_post').value
   });
}
function display_user_input() {
  $('#auto_fill').hide();
  $('#user_fill').show();

}
function validate_user_input() {
  var emotion = document.getElementById('emotion').value;
  var user_post = document.getElementById('user_post').value;
  if (user_post.length > 60) {
    alert("Max char limit exceeded for post");
    return;
  }
  var emotions = ["happy", "sad","irriated", "calm","excited"]
  if (!emotions.includes($("#emotion").val().toLowerCase())){
    alert("Invalid emotion!");
    return;
  }
//   $( "#post_form" ).validate({
//   rules: {
//     user_post: {
//       required: true,
//       max: 60
//     },
//     emotion: {
//       required: function(element) {
//         var emotions = ["happy", "sad","irriated", "calm","excited"]
//         return emotions.includes($("#emotion").val().toLowerCase());
//       }
//     }
//   }
// });
  $('#user_fill').hide();
  $('#posted_string').text("Today I'm " + emotion + " because " + user_post);
  $('#posted_string_block').show();
  $('#post_on_wall').show();
}

function checkContainer (e) {
   e.preventDefault();
   e.stopPropagation();
   var frequency_list = $.get("/graffiti", function(data){
   console.log(data);
//      alert("Data: " + data + "\nStatus: " + status);
   });
  document.getElementById("wall").innerHTML = "";
  if($('#wall').is(':visible')){
     //if the container is visible on the page
    var font_fam = {"sad":"Lucida Console", "happy":"Dancing Script", "depressed":"Saira","irritated":"Saira"};

    var frequency_list = [{"text":"study","size":40, "emotion":"sad"},{"text":"motion","size":15},{"text":"forces","size":10},{"text":"electricity","size":15},{"text":"movement","size":10},{"text":"relation","size":5},{"text":"things","size":10},{"text":"force","size":5},{"text":"ad","size":5},{"text":"energy","size":85},{"text":"living","size":5},{"text":"nonliving","size":5},{"text":"laws","size":15},{"text":"speed","size":45},{"text":"velocity","size":30},{"text":"define","size":5},{"text":"constraints","size":5},{"text":"universe","size":10},{"text":"physics","size":120,"color":"red"},{"text":"describing","size":5},{"text":"matter","size":90, "color":"red", "emotion":"happy"},{"text":"physics-the","size":5},{"text":"world","size":10},{"text":"works","size":10},{"text":"science","size":70},{"text":"interactions","size":30},{"text":"studies","size":5},{"text":"properties","size":45},{"text":"nature","size":40},{"text":"branch","size":30},{"text":"concerned","size":25},{"text":"source","size":40},{"text":"google","size":10},{"text":"defintions","size":5},{"text":"two","size":15},{"text":"grouped","size":15},{"text":"traditional","size":15},{"text":"fields","size":15},{"text":"acoustics","size":15},{"text":"optics","size":15},{"text":"mechanics","size":20},{"text":"thermodynamics","size":15},{"text":"electromagnetism","size":15},{"text":"modern","size":15},{"text":"extensions","size":15},{"text":"thefreedictionary","size":15},{"text":"interaction","size":15},{"text":"org","size":25},{"text":"answers","size":5},{"text":"natural","size":15},{"text":"objects","size":5},{"text":"treats","size":10},{"text":"acting","size":5},{"text":"department","size":5},{"text":"gravitation","size":5},{"text":"heat","size":10},{"text":"light","size":10},{"text":"magnetism","size":10},{"text":"modify","size":5},{"text":"general","size":10},{"text":"bodies","size":5},{"text":"philosophy","size":5},{"text":"brainyquote","size":5},{"text":"words","size":5},{"text":"ph","size":5},{"text":"html","size":5},{"text":"lrl","size":5},{"text":"zgzmeylfwuy","size":5},{"text":"subject","size":5},{"text":"distinguished","size":5},{"text":"chemistry","size":5},{"text":"biology","size":5},{"text":"includes","size":5},{"text":"radiation","size":5},{"text":"sound","size":5},{"text":"structure","size":5},{"text":"atoms","size":5},{"text":"including","size":10}];


    var color = d3.scale.linear()
            .domain([0,1,2,3,4,5,6,10,15,20,100])
            .range(["#ddd", "#ccc", "#bbb", "#aaa", "#999", "#888", "#777", "#666", "#555", "#444", "#333", "#222"]);
    var color = {"default":"green","sad":"yellow", "happy":"pink", "depressed":"grey","irritated":"green", "calm":"blue"}

    var svg = d3.select("#wall").append("svg").attr("width", window.innerWidth)
    .attr("height",window.innerHeight)
    .attr("class", "wordcloud")
    .attr("text-anchor", "middle")
    .style("background", "black");;
    var displaySelection = svg.append("text")
    .attr("font-family", "Lucida Console, Courier, monospace")
    .attr("text-anchor", "start")
    .attr("alignment-baseline", "hanging")
    .attr("x", 10)
    .attr("y", 10);

    d3.layout.cloud().size([window.innerWidth, window.innerHeight])
            .words(frequency_list.map(d => Object.create(d)))
            .padding(10)
            .rotate(() =>0)
            // .rotate(function() {return ~~(Math.random() * 2) * 90;})
            .font(function(d) {if (d.emotion) {return font_fam[d.emotion];} return "serif";})
            .fontSize(function(d) { return d.size; })
            // .color(function(d) {if (d.emotion) {return color[d.emotion];} return "yellow";})
            .text(function(d) { return d.text; })
            // .spiral("rectangular")
            .on("word", ({size, x, y, rotate, text, font, emotion}) => {
              if (!emotion) {
                emotion = "default";
              }

              svg.append("text")
                .attr("font-size", size)
                .attr("font-family", font)
                .attr("fill",color[emotion])
                .attr("transform", `translate(${x},${y}) rotate(${rotate})`)
                .text(text)
                .classed("click-only-text", true)
                .classed("word-default", true)
                .on("mouseover", handleMouseOver)
                .on("mouseout", handleMouseOut)
                .on("click", handleClick);
                function handleMouseOver(d, i) {
                d3.select(this)
                  .classed("word-hovered", true)
                  .transition(`mouseover-${text}`).duration(300).ease("linear")
                    .attr("font-size", size + 5)
                    .attr("font-weight", "bold");
              }

              function handleMouseOut(d, i) {
                d3.select(this)
                  .classed("word-hovered", false)
                  .interrupt(`mouseover-${text}`)
                    .attr("font-size", size);
              }

              function handleClick(d, i) {
                d3.event.stopPropagation();
                var e = d3.select(this);
                $('#exampleModal').modal('show');
                $('#comment_heading').text(`${e.text()}`);
                $('#comment_heading').css("font-size", "50px");
                $('#comment_heading').css("color", "white");
                displaySelection.text(`selection="${e.text()}"`);
                // e.classed("word-selected", !e.classed("word-selected"));
              }
            })
            // .spiral("rectangular")
            .spiral("archimedean")
            .on("end", draw)
            .start();

    function draw(words) {


                svg.append("g")
                // .attr("font-family", function(d) {console.log(d); if (d.emotion) {return font_fam[d.emotion];} return "Impact";})
                // .attr("font-family","Dancing Script,Saira,Impact")
                // without the transform, words words would get cutoff to the left and top, they would
                // appear outside of the SVG area
                .attr("transform", "translate(" + window.innerWidth/2 +","+ window.innerHeight/2 +")");
                // .selectAll("text")
                // .data(words)
                // .enter().append("text")
                // .style("font-family", d=> font_fam[d.emotion])
                // .style("font-size", function(d) { return d.size + "px"; })
                // .style("fill", function(d, i) { if (d.color){return d.color;}return color(i); })
                // .attr("transform", function(d) {
                //     return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                // })
                // .text(function(d) { return d.text; });
    }
    if (e.srcElement.id == "hero") {
      $('#hero').append('<a href="#wall" id="wall_link" class="nav-link scrollto">');
      $('#wall_link')[0].click();
  }

  // $('#auto_fill').show();
  // $('#user_fill').hide();
  // $('#posted_string_block').hide();
  // $('#post_on_wall').hide();
}
}
