"""scrapli_community.ruckus.fastiron.ansync_driver"""

from scrapli.driver import AsyncNetworkDriver


async def default_async_on_open(conn: AsyncNetworkDriver) -> None:
    """
    Async ruckus_fastiron default on_open callable

    Args:
        conn: AsyncNetworkDriver object

    Returns:
        N/A

    Raises:
        N/A
    """
    # When logging in with default credentials, you are prompted to change the password.
    # To keep things simple, we just re-enter the default password for both prompts.
    if conn.auth_username == "super" and conn.auth_password == "sp-admin":
        conn.channel.write(channel_input="sp-admin")
        conn.channel.send_return()
        conn.channel.write(channel_input="sp-admin")
        conn.channel.send_return()
    await conn.acquire_priv(desired_priv=conn.default_desired_privilege_level)
    await conn.send_command(command="skip-page-display")


async def default_async_on_close(conn: AsyncNetworkDriver) -> None:
    """
    Async ruckus_fastiron default on_close callable

    Args:
        conn: AsyncNetworkDriver object

    Returns:
        N/A

    Raises:
        N/A
    """
    # write exit directly to the transport as channel would fail to find the prompt after sending
    # the exit command!
    await conn.acquire_priv(desired_priv=conn.default_desired_privilege_level)
    conn.channel.write(channel_input="exit")
    conn.channel.send_return()
