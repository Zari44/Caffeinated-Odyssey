import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s,%(name)s.%(levelname)s: %(message)s",
)

# important part of each system
logger = logging.getLogger(__name__)
