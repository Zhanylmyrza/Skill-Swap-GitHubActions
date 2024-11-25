import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner
import requests


class ThresholdException(Exception):
    pass


def load_env_variables():
    token = os.getenv("GITHUB_TOKEN")
    gist_id = os.getenv("GITHUB_GIST_ID")

    if not token or not gist_id:
        raise EnvironmentError(
            "Required environment variables GITHUB_TOKEN or GITHUB_GIST_ID are not set"
        )

    return token, gist_id


def generate_coverage_svg(coverage_result):
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="196" height="20">
    <title>Coverage - {coverage_result}%</title>
    
    <defs>
        <linearGradient id="workflow-fill" x1="50%" y1="0%" x2="50%" y2="100%">
        <stop stop-color="#444D56" offset="0%"></stop>
        <stop stop-color="#24292E" offset="100%"></stop>
        </linearGradient>
        <linearGradient id="state-fill" x1="50%" y1="0%" x2="50%" y2="100%">
        <stop stop-color="#34D058" offset="0%"></stop>
        <stop stop-color="#28A745" offset="100%"></stop>
        </linearGradient>
    </defs>
    <g fill="none" fill-rule="evenodd">
        <g font-family="&#39;DejaVu Sans&#39;,Verdana,Geneva,sans-serif" font-size="11">
        <path id="workflow-bg" d="M0,3 C0,1.3431 1.3552,0 3.02702703,0 L146,0 L146,20 L3.02702703,20 C1.3552,20 0,18.6569 0,17 L0,3 Z" fill="url(#workflow-fill)" fill-rule="nonzero"></path>
        <text fill="#010101" fill-opacity=".3">
            <tspan x="22.1981982" y="15" aria-hidden="true">Coverage</tspan>
        </text>
        <text fill="#FFFFFF">
            <tspan x="22.1981982" y="14">Coverage</tspan>
        </text>
        </g>
        <g transform="translate(146)" font-family="&#39;DejaVu Sans&#39;,Verdana,Geneva,sans-serif" font-size="11">
        <path d="M0 0h46.939C48.629 0 50 1.343 50 3v14c0 1.657-1.37 3-3.061 3H0V0z" id="state-bg" fill="url(#state-fill)" fill-rule="nonzero"></path>
        <text fill="#010101" fill-opacity=".3" aria-hidden="true">
            <tspan x="4" y="15">{ coverage_result }%</tspan>
        </text>
        <text fill="#FFFFFF">
            <tspan x="4" y="14">{ coverage_result }%</tspan>
        </text>
        </g>
    </g>

    </svg>
    """


def update_gist(token, gist_id, svg_content):
    payload = {
        "description": "Coverage report",
        "files": {"coverage.svg": {"content": svg_content}},
    }
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    url = f"https://api.github.com/gists/{gist_id}"

    response = requests.patch(url, headers=headers, json=payload)
    response.raise_for_status()
    return response


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.extend([current_dir, os.path.join(current_dir, "backend")])
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "auth_system.settings")
    django.setup()

    try:
        token, gist_id = load_env_variables()
    except EnvironmentError as e:
        print(f"Error: {e}")
        sys.exit(1)

    TestRunner = get_runner(settings)
    test_runner = TestRunner()

    import coverage

    cov = coverage.Coverage()
    cov.start()

    failures = test_runner.run_tests(["accounts"])
    cov.stop()
    coverage_result = cov.report(include="*/views.py")

    svg_content = generate_coverage_svg(coverage_result)
    try:
        update_gist(token, gist_id, svg_content)
        print(f"Coverage report updated successfully: {coverage_result}%")
    except requests.RequestException as e:
        print(f"Failed to update gist: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
