from onedns import exception

from testfixtures import LogCapture


def test_onedns_exception():
    test_msg = "test message"
    e = exception.OneDnsException("test message")
    assert e.msg == test_msg
    assert e.args == (test_msg,)
    assert str(e) == test_msg
    assert e.explain() == 'OneDnsException: {}'.format(test_msg)
    with LogCapture() as log_capture:
        e.log()
        e.log(warn=True)
    log_capture.check(
        ('onedns', 'ERROR', e.explain()),
        ('onedns', 'WARNING', e.explain()),
    )
