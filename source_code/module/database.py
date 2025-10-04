'''
Created on Jan 10, 2017
Modified for OSCE Administration Application - 2025

@author: hanif
'''

import pymysql
import os


class Database:
    def connect(self):
        return pymysql.connect(
            host=os.getenv('DB_HOST', 'aplikasi-kolegium-mysql'),
            user=os.getenv('DB_USER', 'dev'),
            password=os.getenv('DB_PASSWORD', 'dev'),
            database=os.getenv('DB_NAME', 'crud_flask'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    def get_peserta_stats(self):
        """Get statistics for participants including attempt counts"""
        con = self.connect()
        cursor = con.cursor()
        
        try:
            # Get total participants
            cursor.execute("SELECT COUNT(*) as total FROM peserta")
            total_peserta = cursor.fetchone()['total']
            
            # Get participants with first attempt (no previous OSCE records)
            cursor.execute("""
                SELECT COUNT(DISTINCT p.id_peserta) as first_attempt 
                FROM peserta p 
                LEFT JOIN osce_peserta op ON p.id_peserta = op.id_peserta 
                WHERE op.id_peserta IS NULL
            """)
            first_attempt = cursor.fetchone()['first_attempt']
            
            # Get participants with second attempt (has previous OSCE records)
            cursor.execute("""
                SELECT COUNT(DISTINCT p.id_peserta) as second_attempt 
                FROM peserta p 
                INNER JOIN osce_peserta op ON p.id_peserta = op.id_peserta
            """)
            second_attempt = cursor.fetchone()['second_attempt']
            
            # Get universities count
            cursor.execute("SELECT COUNT(*) as total_universities FROM university")
            total_universities = cursor.fetchone()['total_universities']
            
            # Get recent OSCEs
            cursor.execute("""
                SELECT COUNT(*) as total_osce FROM osce 
                WHERE tanggal_osce >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
            """)
            recent_osce = cursor.fetchone()['total_osce']
            
            return {
                'total_peserta': total_peserta,
                'first_attempt': first_attempt,
                'second_attempt': second_attempt,
                'total_universities': total_universities,
                'recent_osce': recent_osce
            }
        except Exception as e:
            print(f"Error getting stats: {e}")
            return {
                'total_peserta': 0,
                'first_attempt': 0,
                'second_attempt': 0,
                'total_universities': 0,
                'recent_osce': 0
            }
        finally:
            con.close()

    def get_recent_peserta(self, limit=10):
        """Get recently added participants"""
        con = self.connect()
        cursor = con.cursor()
        
        try:
            cursor.execute("""
                SELECT p.id_peserta, p.nama, u.nama_universitas, p.email, p.created_at
                FROM peserta p 
                LEFT JOIN university u ON p.universitas = u.id_universitas
                ORDER BY p.created_at DESC 
                LIMIT %s
            """, (limit,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting recent peserta: {e}")
            return []
        finally:
            con.close()
    
    def get_osce_sessions(self):
        """Get all OSCE sessions with participant counts"""
        con = self.connect()
        cursor = con.cursor()
        
        try:
            cursor.execute("""
                SELECT o.id_osce, o.nama_osce, o.tanggal_osce, o.lokasi, o.status,
                       COUNT(p.id_peserta) as participant_count,
                       SUM(CASE WHEN p.status_kelulusan = 'LULUS' THEN 1 ELSE 0 END) as passed_count
                FROM osce o
                LEFT JOIN peserta p ON o.id_osce = p.id_osce
                GROUP BY o.id_osce, o.nama_osce, o.tanggal_osce, o.lokasi, o.status
                ORDER BY o.tanggal_osce DESC
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting OSCE sessions: {e}")
            return []
        finally:
            con.close()
    
    def get_peserta_by_attempt_status(self, attempt_status):
        """Get participants filtered by attempt status (First Attempt/Second Attempt)"""
        con = self.connect()
        cursor = con.cursor()
        
        try:
            cursor.execute("""
                SELECT p.id_peserta, p.nama, u.nama_universitas, p.email, p.no_telp,
                       o.nama_osce, p.status_kelulusan, p.created_at
                FROM peserta p 
                LEFT JOIN university u ON p.universitas = u.id_universitas
                LEFT JOIN osce o ON p.id_osce = o.id_osce
                WHERE p.attempt_status = %s
                ORDER BY p.created_at DESC
            """, (attempt_status,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting peserta by attempt status: {e}")
            return []
        finally:
            con.close()
    
    def get_osce_statistics_by_university(self):
        """Get OSCE statistics grouped by university"""
        con = self.connect()
        cursor = con.cursor()
        
        try:
            cursor.execute("""
                SELECT u.nama_universitas,
                       COUNT(p.id_peserta) as total_participants,
                       SUM(CASE WHEN p.status_kelulusan = 'LULUS' THEN 1 ELSE 0 END) as passed_count,
                       SUM(CASE WHEN p.attempt_status = 'First Attempt' THEN 1 ELSE 0 END) as first_attempt_count,
                       SUM(CASE WHEN p.attempt_status = 'Second Attempt' THEN 1 ELSE 0 END) as second_attempt_count,
                       ROUND((SUM(CASE WHEN p.status_kelulusan = 'LULUS' THEN 1 ELSE 0 END) / COUNT(p.id_peserta)) * 100, 2) as pass_rate
                FROM university u
                LEFT JOIN peserta p ON u.id_universitas = p.universitas
                WHERE p.id_peserta IS NOT NULL
                GROUP BY u.id_universitas, u.nama_universitas
                ORDER BY total_participants DESC
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting OSCE statistics by university: {e}")
            return []
        finally:
            con.close()
