from playwright.sync_api import Page, expect

def set_date(page: Page, input_id: str, hours_offset: int):
    page.evaluate(f"""
        () => {{
            var now = new Date();
            var targetTime = new Date(now.getTime() + {hours_offset} * 60 * 60 * 1000);
            var formattedDate = targetTime.getFullYear() + '/' + 
                                ('0' + (targetTime.getMonth() + 1)).slice(-2) + '/' + 
                                ('0' + targetTime.getDate()).slice(-2);
            var formattedTime = ('0' + targetTime.getHours()).slice(-2) + ':' + 
                                ('0' + targetTime.getMinutes()).slice(-2);
            var dateInput = document.getElementById('{input_id}');
            dateInput.removeAttribute('readonly');
            dateInput.value = formattedDate + ' ' + formattedTime;
            $(dateInput).datetimepicker('setDate', new Date(targetTime));
            $(dateInput).trigger('change');
            dateInput.setAttribute('readonly', 'readonly');
        }}
    """)
