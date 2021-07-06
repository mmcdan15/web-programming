<html>
<body>
%for person in data['people']:
    <br/>
    Hello there, {{person['title'] + ' ' + person['name']}}!
    <br/>
    %if data['holiday']:
        Happy holidays!
    %else:
        Have a nice day!
    %end
    <hr/>
%end
<br/>
</body>
</html>
