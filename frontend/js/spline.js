$(document).ready(function(){
    var draw = SVG('drawing').size($('#drawing').width() - 20, 801);
    var zero_x = 50;
    var zero_y = 400;

    var MAX_DERIVATIVE = 1000;

    var background = draw.rect(draw.width(), draw.height()).fill('none');
    var bar_lines = draw.rect(draw.width(), draw.height()).fill('none');
    var zero_line = draw.line(0, zero_y, draw.width(), zero_y).stroke({color: '#252', width: 3});
    var plus_one_line = draw.line().stroke({color: '#f88', width: 2});
    var minus_one_line = draw.line().stroke({color: '#88f', width: 2});
    var axis_label = draw.group();
    var active_key = axis_label.rect().fill('#ccc');
    var control_lines = draw.path().fill('none').stroke({color: 'green', width: 1});

    function update_grid(){
        var x = $('#snap_x').val();
        var y = $('#snap_y').val();
        var pattern = draw.pattern(x, y, function(add){
            add.polyline([[0, y], [0, 0], [x, 0]]).fill('none').stroke({color: '#335', width: 1});
        });
        pattern.move(zero_x, zero_y);
        background.fill(pattern);

        var bar = $('#bar').val();
        if (bar <= 0){
            bar_lines.fill('none');
        }
        else {
            var pattern = draw.pattern(x * bar, y, function(add){
                add.line(1, 0, 1, y).stroke({width: 2});
            });
            pattern.move(zero_x - 1, zero_y);
            bar_lines.fill(pattern);
        }
    }
    update_grid();
    $('#snap_x').change(update_grid);
    $('#snap_y').change(update_grid);
    $('#bar').change(update_grid);

    function use_pitch(){
        return $('input[name=real_pitch]:checked').val() == 'pitch';
    }

    function update_unity(){
        if (use_pitch()){
            plus_one_line.hide();
            minus_one_line.hide();
        }
        else {
            var unity = $('#unity').val() | 0;
            plus_one_line.plot(0, zero_y - unity, draw.width(), zero_y - unity).show();
            minus_one_line.plot(0, zero_y + unity, draw.width(), zero_y + unity).show();
        }
    }
    $('#unity').change(update_unity).change();
    $('input[name=real_pitch]').change(update_unity);

    function update_axis(){
        axis_label.clear();
        var y = $('#snap_y').val() | 0;
        if (use_pitch()){
            var pattern = draw.pattern(zero_x, y * 12, function(add){
                add.rect(zero_x, y * 1.5).move(0, 0.0 * y).fill('white').stroke({width: 1});
                add.rect(zero_x, y * 2.0).move(0, 1.5 * y).fill('white').stroke({width: 1});
                add.rect(zero_x, y * 2.0).move(0, 3.5 * y).fill('white').stroke({width: 1});
                add.rect(zero_x, y * 1.5).move(0, 5.5 * y).fill('white').stroke({width: 1});
                add.rect(zero_x, y * 1.5).move(0, 7.0 * y).fill('white').stroke({width: 1});
                add.rect(zero_x, y * 2.0).move(0, 8.5 * y).fill('white').stroke({width: 1});
                add.rect(zero_x, y * 1.5).move(0, 10.5 * y).fill('white').stroke({width: 1});

                blacks = add.group();
                blacks.rect(zero_x * 0.8, y * 0.8).move(0, 1 * y).fill('black').stroke({width: 1});
                blacks.rect(zero_x * 0.8, y * 0.8).move(0, 3 * y).fill('black').stroke({width: 1});
                blacks.rect(zero_x * 0.8, y * 0.8).move(0, 5 * y).fill('black').stroke({width: 1});
                blacks.rect(zero_x * 0.8, y * 0.8).move(0, 8 * y).fill('black').stroke({width: 1});
                blacks.rect(zero_x * 0.8, y * 0.8).move(0, 10 * y).fill('black').stroke({width: 1});
                blacks.move(0, 0.1 * y);
            });
            pattern.move(0, zero_y + y / 2);
            axis_label.rect(zero_x, draw.height()).fill(pattern);
            active_key = axis_label.rect().fill('#ccc');
        }
        else {
            var unity = $('#unity').val() | 0;
            axis_label.rect(zero_x, draw.height()).fill('#f9f9f9');
            var ty = zero_y;
            var t = 0;
            while (ty > 0){
                axis_label.plain(t.toFixed(2)).move(0, ty - y / 2);
                t += y / unity;
                ty -= y;
            }
            var ty = zero_y + y;
            var t = -y / unity;
            while (ty + 1 < draw.height()){
                axis_label.plain(t.toFixed(2)).move(0, ty - y / 2);
                t -= y / unity;
                ty += y;
            }
        }
    }
    update_axis();
    $('input[name=real_pitch]').change(update_axis);
    $('#snap_y').change(update_axis);
    $('#unity').change(update_axis);

    function create_marker(parent, point){
        var circle = parent.circle(10).move(point[0] - 5, point[1] - 5).fill('blue');
        axis_label.front();
        return circle;
    }

    var pointss = [];
    var markerss = [];
    var curves = [];
    var curve_types = [];
    var curve_index = -1;

    var points;
    var polyline;
    var path;
    var curve_type;
    var markers;

    function update_marker(i){
        markers[i].center(points[i][0], points[i][1]);
    }

    function limit_derivative(d){
        if (isNaN(d)){
            return 0;
        }
        else{
            return Math.max(-MAX_DERIVATIVE, Math.min(MAX_DERIVATIVE, d));
        }
    }

    function update_curve(){
        if (curve_type == 'polyline'){
            polyline.plot(points);
        }
        else{
            path_data = [['M', points[0][0], points[0][1]]];
            for (var i = 1; i < points.length; i += 3){
                var l = (points[i + 2][0] - points[i - 1][0]) / 3;
                var d1 = (points[i][1] - points[i - 1][1]) / (points[i][0] - points[i - 1][0]);
                d1 = limit_derivative(d1);
                var x1 = points[i - 1][0] + l;
                var y1 = points[i - 1][1] + d1 * l;
                var d2 = (points[i + 2][1] - points[i + 1][1]) / (points[i + 2][0] - points[i + 1][0]);
                d2 = limit_derivative(d2);
                var x2 = points[i + 2][0] - l;
                var y2 = points[i + 2][1] - d2 * l;
                path_data.push(['C', x1, y1, x2, y2, points[i + 2][0], points[i + 2][1]]);
            }
            path.plot(path_data);

            path_data = [['M', points[0][0], points[0][1]]];
            for (var i = 0; i < points.length; i += 3){
                if (i > 0){
                    path_data.push(['M', points[i - 1][0], points[i -1][1]]);
                    path_data.push(['L', points[i][0], points[i][1]]);
                }
                if (i < points.length - 1){
                    path_data.push(['L', points[i + 1][0], points[i + 1][1]]);
                }
            }
            control_lines.plot(path_data);
        }
    }

    function deactivate_curve(){
        $(curves).each(function(i, curve){
            curve.stroke({color: 'gray'});
        });
        $(markers).each(function(i, marker){
            if (curve_type == 'bezier' && i % 3 != 0){
                marker.hide();
            }
            else {
                marker.fill('gray');
            }
        });
        control_lines.hide();
    }

    function activate_curve(){
        points = pointss[curve_index];
        curve_type = curve_types[curve_index];
        if (curve_type == 'polyline'){
            polyline = curves[curve_index];
            polyline.stroke({color: 'black'});
        }
        else {
            path = curves[curve_index];
            path.stroke({color: 'black'});
            control_lines.show();
            update_curve();
        }
        markers = markerss[curve_index];
        $(markers).each(function(i, marker){
            marker.show();
            marker.fill('blue');
        });
    }

    function new_line(){
        deactivate_curve();
        points = [[200, 200], [400, 200]];
        pointss.push(points);
        polyline = draw.polyline().fill('none').stroke({width: 1});
        curves.push(polyline);
        curve_type = 'polyline';
        curve_types.push(curve_type);
        update_curve();
        markers = [];
        markerss.push(markers);
        $(points).each(function(i, point){
            markers.push(create_marker(draw, point));
        });
        curve_index = pointss.length - 1;
    }

    function new_bezier(){
        deactivate_curve();
        points = [[200, 200], [300, 300], [400, 300], [500, 200]];
        pointss.push(points);
        path = draw.path().fill('none').stroke({width: 1});
        curves.push(path);
        curve_type = 'bezier';
        curve_types.push(curve_type);
        control_lines.show();
        update_curve();
        markers = [];
        markerss.push(markers);
        $(points).each(function(i, point){
            markers.push(create_marker(draw, point));
        });
        curve_index = pointss.length - 1;
    }

    function next_curve(){
        deactivate_curve();
        curve_index++;
        if (curve_index >= pointss.length){
            curve_index = 0;
        }
        activate_curve();
    }

    function previous_curve(){
        deactivate_curve();
        curve_index--;
        if (curve_index < 0){
            curve_index = pointss.length - 1;
        }
        activate_curve();
    }

    function delete_curve(){
        if (curve_type == 'polyline'){
            polyline.remove();
        }
        else {
            path.remove();
        }
        $(markers).each(function(i, marker){
            marker.remove();
        });
        pointss.splice(curve_index, 1);
        curves.splice(curve_index, 1);
        curve_types.splice(curve_index, 1);
        markerss.splice(curve_index, 1);
        if (pointss.length <= 0){
            if (curve_type == 'polyline'){
                new_bezier();
            }
            else{
                new_line();
            }
        }
        if (curve_index >= pointss.length){
            curve_index = 0;
        }
        activate_curve();
    }

    new_line();
    $('#new_line').click(new_line);
    $('#new_bezier').click(new_bezier);
    $('#next').click(next_curve);
    $('#previous').click(previous_curve);
    $('#delete').click(delete_curve);

    $('#get_data').click(function(){
        var y = $('#snap_y').val() | 0;
        var unity = $('#unity').val() | 0;
        var result = '';
        $(points).each(function(i, point){
            if (i == 0){
                result += '[';
            }
            else {
                result += ',';
            }
            result += (point[0] - zero_x) + ',';
            if (use_pitch()){
                result += (zero_y - point[1]) / y;
            }
            else {
                result += (zero_y - point[1]) / unity;
            }
        });
        result += ']';
        $('#output').val(result);
    });

    var active_index = 0;
    var edit_mode = false;
    var add_mode = false;
    var delete_mode = false;

    $(window).keydown(function(event){
        if (event.altKey){
            balance_control_points(event);
        }
        /*
        if (event.ctrlKey){
            add_mode = true;
        }
        if (event.shiftKey){
            delete_mode = true;
        }
        */
    });
    /*
    $(window).keyup(function(event){
        if (event.keyCode == 17){
            add_mode = false;
        }
        else if (event.keyCode == 16){
            delete_mode = false;
        }
    });
    */

    function snap_x(x){
        if ($('#snap_x_check').is(':checked')){
            var snap = $('#snap_x').val();
            return Math.round((x - zero_x) / snap) * snap + zero_x;
        }
        else{
            return x;
        }
    }

    function snap_y(y){
        if ($('#snap_y_check').is(':checked')){
            var snap = $('#snap_y').val();
            return Math.round((y - zero_y) / snap) * snap + zero_y;
        }
        else{
            return y;
        }
    }

    function highlight_active_key(event){
        if (use_pitch()){
            var snap = $('#snap_y').val();
            var key = Math.round((event.offsetY - zero_y) / snap) 
            var y = key * snap + zero_y;
            key -= Math.floor(key / 12) * 12;
            if (key == 2 || key == 4 || key == 6 || key == 9 || key == 11){
                active_key.size(zero_x * 0.75, snap * 0.5).move(0, y - snap * 0.25);
            }
            else{
                active_key.size(zero_x * 0.95, snap * 0.6).move(0, y - snap * 0.3);
            }
        }
    }

    function control_point_active(){
        if (curve_type == 'polyline'){
            return false;
        }
        else{
            var t = active_index % 3;
            return t == 1 || t == 2;
        }
    }

    function balance_control_points(event){
        if (control_point_active() && event.altKey){
            var t = active_index % 3;
            if (t == 1 && active_index > 1){
                var d = (points[active_index][1] - points[active_index - 1][1]) / (points[active_index][0] - points[active_index - 1][0]);
                d = limit_derivative(d);
                points[active_index - 2][1] = points[active_index - 1][1] - d * (points[active_index - 1][0] - points[active_index - 2][0]);
                update_marker(active_index - 2);
            }
            else if (t == 2 && active_index < points.length - 2){
                var d = (points[active_index + 1][1] - points[active_index][1]) / (points[active_index + 1][0] - points[active_index][0]);
                d = limit_derivative(d);
                points[active_index + 2][1] = points[active_index + 1][1] + d * (points[active_index + 2][0] - points[active_index + 1][0]);
                update_marker(active_index + 2);
            }
            update_curve();
        }
    }

    function move_active_point(event){
        var x = event.offsetX;
        var y = event.offsetY;
        if (!control_point_active()){
            x = snap_x(x);
            y = snap_y(y);
        }
        if (active_index > 0){
            if (x < points[active_index - 1][0]){
                x = points[active_index - 1][0];
            }
        }
        if (active_index < points.length - 1){
            if (x > points[active_index + 1][0]){
                x = points[active_index + 1][0];
            }
        }
        points[active_index] = [x, y];
        if (curve_type == 'bezier' && !control_point_active()){
            if (active_index > 0){
                points[active_index - 1][0] = (2 * points[active_index][0] + points[active_index - 3][0]) / 3;
                points[active_index - 2][0] = (points[active_index][0] + 2 * points[active_index - 3][0]) / 3;
                update_marker(active_index - 1);
                update_marker(active_index - 2);
            }
            if (active_index < points.length - 1){
                points[active_index + 1][0] = (2 * points[active_index][0] + points[active_index + 3][0]) / 3;
                points[active_index + 2][0] = (points[active_index][0] + 2 * points[active_index + 3][0]) / 3;
                update_marker(active_index + 1);
                update_marker(active_index + 2);
            }
        }
        update_curve();
        update_marker(active_index);
    }

    function find_active_point(event){
        markers[active_index].fill('blue');
        var min_distance = Infinity;
        $(points).each(function(i, point){
            var distance = Math.pow(point[0] - event.offsetX, 2) + Math.pow(point[1] - event.offsetY, 2);
            if (distance < min_distance){
                active_index = i;
                min_distance = distance;
            }
        });
        markers[active_index].fill('red');
    }

    function create_point(event){
        markers[active_index].fill('blue');
        var x = event.offsetX;
        var y = event.offsetY;
        x = snap_x(x);
        y = snap_y(y);
        if (curve_type == 'polyline'){
            $(points).each(function(i, point){
                if (point[0] > x){
                    points.splice(i, 0, [x, y]);
                    markers.splice(i, 0, create_marker(draw, [x, y]));
                    active_index = i;
                    return false;
                }
            });
            if (x >= points[points.length - 1][0]){
                points.push([x, y]);
                markers.push(create_marker(draw, [x, y]));
                active_index = points.length - 1;
            }
        }
        else {
            if (x < points[0][0]){
                var l = (points[0][0] - x) / 3;
                var p0 = [x, y];
                var p1 = [x + l, y];
                var p2 = [points[0][0] - l, points[0][1]];
                points.splice(0, 0, p0, p1, p2);
                markers.splice(0, 0, create_marker(draw, p0), create_marker(draw, p1), create_marker(draw, p2));
                active_index = 0;
            }
            else if (x > points[points.length - 1][0]){
                var i = points.length - 1;
                var l = (x - points[i][0]) / 3;
                var p1 = [points[i][0] + l, points[i][1]];
                var p2 = [x - l, y];
                var p3 = [x, y];
                points.splice(i + 1, 0, p1, p2, p3);
                markers.splice(i + 1, 0, create_marker(draw, p1), create_marker(draw, p2), create_marker(draw, p3));
                active_index = i + 1;
            }
            else {
                $(points).each(function(i, point){
                    if (i % 3 == 0 && point[0] > x){
                        var l0 = (point[0] - x) / 3;
                        var l1 = (x - points[i - 3][0]) / 3;
                        points[i - 2][0] = points[i - 3][0] + l0;
                        update_marker(i - 2);
                        var p2 = [x - l0, y];
                        var p3 = [x, y];
                        var p4 = [x + l1, y];
                        points[i - 1][0] = point[0] - l1;
                        update_marker(i - 1);
                        points.splice(i - 1, 0, p2, p3, p4);
                        markers.splice(i - 1, 0, create_marker(draw, p2), create_marker(draw, p3), create_marker(draw, p4));
                        active_index = i;
                        return false;
                    }
                });
            }
        }
        update_curve();
        find_active_point(event);
    }

    function delete_point(event){
        if (points.length <= 2){
            return;
        }
        if (control_point_active() || points.length <= 4){
            return;
        }
        if (curve_type == 'polyline'){
            points.splice(active_index, 1);
            markers[active_index].remove();
            markers.splice(active_index, 1);
        }
        else{
            if (active_index == points.length - 1){
                points.splice(active_index - 2, 3);
                markers[active_index - 2].remove();
                markers[active_index - 1].remove();
                markers[active_index].remove();
                markers.splice(active_index - 2, 3);
            }
            else if (active_index == 0){
                points.splice(active_index , 3);
                markers[active_index].remove();
                markers[active_index + 1].remove();
                markers[active_index + 2].remove();
                markers.splice(active_index, 3);
            }
            else {
                points.splice(active_index - 1, 3);
                markers[active_index - 1].remove();
                markers[active_index].remove();
                markers[active_index + 1].remove();
                markers.splice(active_index - 1, 3);
            }
        }
        update_curve();
        if (active_index >= points.length){
            active_index = points.length - 1;
        }
        find_active_point(event);
    }

    draw.on('mousedown', function(event){
        event.preventDefault();
        add_mode = event.ctrlKey;
        delete_mode = event.shiftKey;

        if (add_mode){
            create_point(event);
            edit_mode = true;
            move_active_point(event);
        }
        else if (delete_mode){
            delete_point(event);
        }
        else{
            edit_mode = true;
            move_active_point(event);
        }
    });
    draw.on('mouseup', function(event){
        edit_mode = false;
    });

    SVG.on(window, 'mousemove', function(event){
        highlight_active_key(event);
        if (edit_mode){
            move_active_point(event);
        }
        else {
            find_active_point(event);
        }
        balance_control_points(event);
    });
});
