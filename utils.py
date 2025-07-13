from config import HEALTH_THRESHOLDS, EMOJIS
from datetime import datetime, timedelta

def get_health_emoji(value, metric_type):
    """
    Get health emoji based on value and metric type
    
    Args:
        value: The value to check
        metric_type: Type of metric (cpu, ram, disk, ping, players)
        
    Returns:
        str: Emoji representing health status
    """
    if value is None:
        return EMOJIS['offline']
    
    thresholds = HEALTH_THRESHOLDS.get(metric_type, {})
    good_threshold = thresholds.get('good', 50)
    moderate_threshold = thresholds.get('moderate', 80)
    
    if value < good_threshold:
        return EMOJIS['good']
    elif value < moderate_threshold:
        return EMOJIS['moderate']
    else:
        return EMOJIS['critical']

def get_overall_health(lavalink_data, system_data):
    """
    Calculate overall health status
    
    Args:
        lavalink_data: List of Lavalink node data
        system_data: System statistics
        
    Returns:
        str: Overall health status (good, moderate, critical)
    """
    critical_count = 0
    moderate_count = 0
    total_metrics = 0
    
    # Check Lavalink nodes
    for node in lavalink_data:
        if node.get('online', False):
            stats = node['stats']
            
            # CPU check
            cpu_emoji = get_health_emoji(stats['cpu'] * 100, 'cpu')
            if cpu_emoji == EMOJIS['critical']:
                critical_count += 1
            elif cpu_emoji == EMOJIS['moderate']:
                moderate_count += 1
            total_metrics += 1
            
            # RAM check
            ram_percent = stats['memory']['used'] / stats['memory']['allocated'] * 100
            ram_emoji = get_health_emoji(ram_percent, 'ram')
            if ram_emoji == EMOJIS['critical']:
                critical_count += 1
            elif ram_emoji == EMOJIS['moderate']:
                moderate_count += 1
            total_metrics += 1
            
            # Ping check
            ping_emoji = get_health_emoji(node.get('ping', 999), 'ping')
            if ping_emoji == EMOJIS['critical']:
                critical_count += 1
            elif ping_emoji == EMOJIS['moderate']:
                moderate_count += 1
            total_metrics += 1
    
    # Check system stats
    if system_data:
        system_cpu_emoji = get_health_emoji(system_data['cpu_percent'], 'cpu')
        if system_cpu_emoji == EMOJIS['critical']:
            critical_count += 1
        elif system_cpu_emoji == EMOJIS['moderate']:
            moderate_count += 1
        total_metrics += 1
        
        system_ram_emoji = get_health_emoji(system_data['memory_percent'], 'ram')
        if system_ram_emoji == EMOJIS['critical']:
            critical_count += 1
        elif system_ram_emoji == EMOJIS['moderate']:
            moderate_count += 1
        total_metrics += 1
        
        system_disk_emoji = get_health_emoji(system_data['disk_percent'], 'disk')
        if system_disk_emoji == EMOJIS['critical']:
            critical_count += 1
        elif system_disk_emoji == EMOJIS['moderate']:
            moderate_count += 1
        total_metrics += 1
    
    # Determine overall health
    if total_metrics == 0:
        return 'critical'
    
    critical_ratio = critical_count / total_metrics
    moderate_ratio = moderate_count / total_metrics
    
    if critical_ratio > 0.3:  # More than 30% critical
        return 'critical'
    elif critical_ratio > 0.1 or moderate_ratio > 0.5:  # More than 10% critical or 50% moderate
        return 'moderate'
    else:
        return 'good'

def format_uptime(seconds):
    """
    Format uptime in seconds to human-readable format
    
    Args:
        seconds: Uptime in seconds
        
    Returns:
        str: Formatted uptime string
    """
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    elif seconds < 86400:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"
    else:
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        return f"{days}d {hours}h"

def format_bytes(bytes_value):
    """
    Format bytes to human-readable format
    
    Args:
        bytes_value: Size in bytes
        
    Returns:
        str: Formatted size string
    """
    if bytes_value < 1024:
        return f"{bytes_value}B"
    elif bytes_value < 1024**2:
        return f"{bytes_value / 1024:.1f}KB"
    elif bytes_value < 1024**3:
        return f"{bytes_value / (1024**2):.1f}MB"
    else:
        return f"{bytes_value / (1024**3):.1f}GB"

def get_status_color(health_status):
    """
    Get Discord embed color based on health status
    
    Args:
        health_status: Health status (good, moderate, critical)
        
    Returns:
        int: Discord color code
    """
    colors = {
        'good': 0x00ff00,      # Green
        'moderate': 0xff8800,  # Orange
        'critical': 0xff0000,  # Red
        'offline': 0x808080    # Gray
    }
    
    return colors.get(health_status, colors['offline'])

def truncate_string(text, max_length=100):
    """
    Truncate string to maximum length with ellipsis
    
    Args:
        text: String to truncate
        max_length: Maximum length
        
    Returns:
        str: Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."

def format_timestamp(timestamp):
    """
    Format timestamp to readable format
    
    Args:
        timestamp: Unix timestamp or datetime object
        
    Returns:
        str: Formatted timestamp
    """
    if isinstance(timestamp, (int, float)):
        dt = datetime.fromtimestamp(timestamp)
    else:
        dt = timestamp
    
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def calculate_percentage(value, total):
    """
    Calculate percentage with error handling
    
    Args:
        value: Current value
        total: Total value
        
    Returns:
        float: Percentage (0-100)
    """
    if total == 0:
        return 0.0
    return (value / total) * 100

def get_load_indicator(load_avg, cpu_count):
    """
    Get load average indicator
    
    Args:
        load_avg: System load average
        cpu_count: Number of CPU cores
        
    Returns:
        str: Load indicator emoji
    """
    if cpu_count == 0:
        return EMOJIS['offline']
    
    load_percentage = (load_avg / cpu_count) * 100
    
    if load_percentage < 70:
        return EMOJIS['good']
    elif
