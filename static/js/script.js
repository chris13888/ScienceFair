let filter = new RegExp('a^', 'g');

function message(messagetext){
  console.log('message showing up');
  let el = $('#snack');
  el.html(messagetext);
  el.removeClass('dismiss');
  el.addClass('show');
}

function copy(){
  console.log('copied');
  $('#text').select();
  document.execCommand('copy');
  window.getSelection().removeAllRanges();
  message('Copied to your clipboard!');
}

function dismiss(){
  let el = $('#snack');
  el.removeClass('show');
  el.addClass('dismiss');
}

function change_find(){
  let raw = $('#find').val();
  if (raw.startsWith('re:')){
    raw = raw.substring(3).split(':flags:');
    let mod = 'g';
    if (raw.length > 1){mod = 'g'+raw[1].replace('|', '');}
    filter = new RegExp(raw[0], mod);
  }else{
    filter = new RegExp(raw.replace('\\', '\\\\'), 'gi');
  }
  handle_press();
}

function change_text(){
  change_find();

  let replace_text = $('#replace').val()
  let original_text = $('#text').val()
  $('#text').val(original_text.replace(filter, replace_text));

  console.log(replace_text);

  handle_press();
}

function noenter(that) {
  if (window.event && window.event.keyCode == 13){
    if ($(that).attr('id') == 'find'){
      change_find();
    } else {
      change_text();
    }
  };
  return !(window.event && window.event.keyCode == 13);
}

function highlight(text){
  let newtext = text.replace(filter, (m) => `<span class="highlight">${m}</span>`.replace(/\n/g, '<br>'));
  return newtext+'\n\n';
}

function handle_press(){
  let text = $('#text').val();
  $('#highlighter').html(highlight(text));
}

function handle_scroll() {
  $('#backdrop').scrollTop($('#text').scrollTop());
  $('#backdrop').scrollLeft($('#text').scrollLeft());
}

$(document).ready(function(){
  $('#text').on({
    'input': handle_press,
    'scroll': handle_scroll
  });

  message('Start with the prefix re: to create a regex filter! <br>You can add :flags: and some pipeline seperated flags at the end!')
})

function add(element){
	e = $(element);
	/* console.log(e.parent()) */
  e.parent().children().eq(0).children().eq(0).children().eq(0).prepend('<td class="author-name">Author Name<br><span style="font-size: 0.7em;">(Lastname, Firstname)</span></td>');
	e.parent().children().eq(0).children().eq(0).children().eq(1).prepend('<td><input class="input author-field"/></td>');
	/* e.parent().first().first().prepend('<td>Incredible</td>') */
}

function delet(element){
	e = $(element);

  if (e.parent().children().eq(0).children().eq(0).children().eq(0).children().eq(0).hasClass('author-name')){
    e.parent().children().eq(0).children().eq(0).children().eq(0).children().eq(0).remove();
    e.parent().children().eq(0).children().eq(0).children().eq(1).children().eq(0).remove();
  }
}

function cite(element){
  let article_field = '';
  let site_field = '';
  let url_field = '';
  let months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  let today = new Date();
  let author = [];
  let e = $(element);
  e.parent().children().eq(0).children().eq(0).children().eq(1).children().each(function(){
    let el = $(this).children().eq(0);
    console.log(el.hasClass('author-field'), el.hasClass('article-field'), el.hasClass('site-field'), el.hasClass('url-field'));
    if (el.hasClass('author-field')){
      author.push(el.val());
    }else if (el.hasClass('article-field')){
      article_field = el.val();
    }else if (el.hasClass('site-field')){
      site_field = el.val();
    }else{
      url_field = el.val();
    }
  });
  let mla = '';
  let apa = '';
  if (author.length == 1){
    apa += author[0].split(', ')[0]+', '+author[0].split(', ')[1][0]+'. ';
    mla += author[0];
  }else if (author.length == 2){
    apa += author[0].split(', ')[0]+', '+author[0].split(', ')[1][0]+'., & ';
    apa += author[1].split(', ')[0]+', '+author[1].split(', ')[1][0]+'. ';
    mla += author[0]+', and '+author[1].split(', ').reverse().join(' ');
  }else if (author.length > 2){
    for (var i = 0; i<author.length-1; i+=1){
      apa += author[i].split(', ')[0]+', '+author[i].split(', ')[1][0]+'., ';
    }
    apa += '& '+author[author.length-1].split(', ')[0]+', '+author[author.length-1].split(', ')[1][0]+'. ';
    mla += author[0]+', et al. '
  }
  apa += article_field+'. ';
  mla += '"'+article_field+'." ';
  apa += '<i>'+site_field+'</i>. ';
  mla += '<i>'+site_field+'</i>, '+url_field+'. ';
  apa += 'Retrieved from '+url_field+'. ';
  mla += 'Accessed '+today.getDate()+' '+months[today.getMonth()]+' '+today.getFullYear()+'.';
  e.parent().children().eq(-4).html('<div class="bordered" style="padding: 1em;">Citation generated! <br><b>MLA</b>: '+mla+'<br><b>APA</b>: '+apa+'</div><br>');
}
