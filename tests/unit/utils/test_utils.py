from project_template.utils.utils import get_tos_version_and_hash


def test_get_tos_version():
    version, hash_ = get_tos_version_and_hash(
        """
**Version: 2.11**
test
    """
    )
    assert version == "2.11"
    assert hash_ == "8a0172dbe7acc3acad1ace83549cb67f"
