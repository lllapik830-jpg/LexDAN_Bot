"""
Гарантия одного polling-инстанса.

На Render при деплое/двух сервисах иначе ловим:
TelegramConflictError: terminated by other getUpdates request
"""

from __future__ import annotations

import logging
import os
import time

log = logging.getLogger(__name__)

# Стабильный ключ advisory lock для этого бота
_LOCK_KEY = 8827357777


def _use_postgres() -> bool:
    return bool((os.getenv("DATABASE_URL") or "").strip())


def _pg_connect():
    import psycopg

    url = (os.getenv("DATABASE_URL") or "").strip()
    if "sslmode=" not in url:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}sslmode=require"
    return psycopg.connect(url)


_conn = None


def try_acquire_bot_lock() -> bool:
    """True — этот процесс может запускать polling."""
    global _conn
    if not _use_postgres():
        # Локально без PG — файловый lock
        return _try_file_lock()
    try:
        if _conn is None or _conn.closed:
            _conn = _pg_connect()
            _conn.autocommit = True
        with _conn.cursor() as cur:
            cur.execute("SELECT pg_try_advisory_lock(%s)", (_LOCK_KEY,))
            row = cur.fetchone()
            ok = bool(row and row[0])
        if ok:
            log.info("Bot polling lock acquired (postgres advisory)")
        else:
            log.warning("Bot polling lock busy — another instance is running")
        return ok
    except Exception as e:
        log.error("Bot lock acquire failed: %s — allowing start", e)
        return True


def release_bot_lock() -> None:
    global _conn
    if not _use_postgres():
        _release_file_lock()
        return
    if _conn is None or _conn.closed:
        return
    try:
        with _conn.cursor() as cur:
            cur.execute("SELECT pg_advisory_unlock(%s)", (_LOCK_KEY,))
        log.info("Bot polling lock released")
    except Exception as e:
        log.warning("Bot lock release failed: %s", e)
    try:
        _conn.close()
    except Exception:
        pass
    _conn = None


_FILE_LOCK_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".bot_poll.lock")
_file_fh = None


def _try_file_lock() -> bool:
    global _file_fh
    try:
        _file_fh = open(_FILE_LOCK_PATH, "w", encoding="utf-8")
        try:
            import msvcrt

            msvcrt.locking(_file_fh.fileno(), msvcrt.LK_NBLCK, 1)
        except ImportError:
            import fcntl

            fcntl.flock(_file_fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        _file_fh.write(str(os.getpid()))
        _file_fh.flush()
        log.info("Bot polling lock acquired (file)")
        return True
    except Exception as e:
        log.warning("Bot polling lock busy (file): %s", e)
        try:
            if _file_fh:
                _file_fh.close()
        except Exception:
            pass
        _file_fh = None
        return False


def _release_file_lock() -> None:
    global _file_fh
    if not _file_fh:
        return
    try:
        try:
            import msvcrt

            _file_fh.seek(0)
            msvcrt.locking(_file_fh.fileno(), msvcrt.LK_UNLCK, 1)
        except ImportError:
            import fcntl

            fcntl.flock(_file_fh.fileno(), fcntl.LOCK_UN)
        _file_fh.close()
    except Exception:
        pass
    _file_fh = None


async def wait_for_bot_lock(*, max_wait_sec: int = 120) -> bool:
    """Ждём освобождения лока (старый инстанс при деплое)."""
    import asyncio

    deadline = time.time() + max_wait_sec
    while time.time() < deadline:
        if try_acquire_bot_lock():
            return True
        await asyncio.sleep(3)
    return try_acquire_bot_lock()
