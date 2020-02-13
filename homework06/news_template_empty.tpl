<!DOCTYPE html>
<html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/jquery@3.3.1/dist/jquery.min.js"></script>
        <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/fomantic-ui@2.8.3/dist/semantic.min.css">
        <script src="https://cdn.jsdelivr.net/npm/fomantic-ui@2.8.3/dist/semantic.min.js"></script>
        <style>
            body {
                background: #4079b1;
            }
        </style>
        <!--
            table {
                border-collapse: collapse;
            }
            tr, td {
                padding: 0;
            }
            tr td div {
                max-height: 0px;
                padding: 0 10px;
                box-sizing: border-box;
                overflow: hidden;
                transition: max-height 0.3s, padding 0.3s;
            }
            tr.active1 td div {
                max-height: 50px;
                padding: 10px 10px;
                transition: max-height 0.6s, padding 0.6s;
            }
        -->
            
        

        
    </head>
    <body>
        <div class="ui container" style="padding-top: 10px;">
            <div class="ui inverted placeholder segment">
                <div class="ui icon header">
                    <i class="search icon"></i>
                    Looks like no more news in database
                </div>
                <div class="inline">
                    <a href="/update" class="ui primary button">Add 30 more</a>
                    <div class="ui button">Clear Query</div>
                </div>
            </div>
        </div>
    </body>
</html>
