$('form input[type="file"]').each(function() {
          var upload = $(this);
          upload.wrap("<span class='upload-hide'></span>");
          var styledUpload = "<span class='styled-upload' data-value='"+upload.val().split('\\').pop()+"' data-name='"+upload.attr('name')+"'><span class='file'></span><span class='upload primary'>Choose File</span></span></span></span>";
          upload.parent('.upload-hide').after(styledUpload);
        });

        $('.styled-upload .upload').on('click', function () {
          var upload = $('input[type="file"][name="'+$(this).parent().attr('data-name')+'"]');
          upload.click();
        });

        $('form input[type="file"]').on('change', function () {
          var upload = $(this);
          var file = upload.val().split('\\').pop();
          if (file !== "") {
            upload.parent().next('.styled-upload').find('.file').addClass('show').text(file);
          } else {
            upload.parent().next('.styled-upload').find('.file').text("");
          }
        });

        $('.styled-upload .file').on('click', function() {
          var upload = $('input[type="file"][name="'+$(this).parent().attr('data-name')+'"]');
          upload.val("");
          $(this).removeClass('show');
          upload.change();
        });