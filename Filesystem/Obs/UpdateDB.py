import os
import sqlite3
import pickle
import shutil

class DB :

    def construct(self, u_info):
        id_tile_list = []
        id_max = 0
        id_counts = np.zeros(0, dtype=np.int64)
        for iw in range(self.num_tiles_w):
            for iz, iy, ix in itertools.product(range(self.num_tiles_z), range(self.num_tiles_y_at_w[iw]),
                                            range(self.num_tiles_x_at_w[iw])):

        ### Load tile file
        ### tile_ids( ( tile_num_pixels_y, tile_num_pixels_x ), np.uint32 )

                tile_ids_filename = u_info.mojo_tile_ids_path + u_info.tile_ids_filename_wzyx.format(iw, iz, iy, ix)
                tile_ids = load_hdf5(tile_ids_filename, u_info.tile_var_name)
                unique_tile_ids = np.unique(tile_ids)

                ## Update database

                # Max id
                current_max = np.max(unique_tile_ids)
                if id_max < current_max:
                    id_max = current_max
                    id_counts.resize(id_max + 1)
                    # print id_max

                # id list
                for unique_tile_id in unique_tile_ids:
                    id_tile_list.append((unique_tile_id, id_w, iz, iy, ix))

                # Pixel number of each id
                if iw == 0:
                    current_ids_counts = np.bincount(tile_ids.ravel())
                    current_ids_counts_ids = np.nonzero(current_ids_counts)[0]
                    id_counts[current_ids_counts_ids] = \
                        id_counts[current_ids_counts_ids] + np.int64(current_ids_counts[current_ids_counts_ids])

    ## Max color number check
        if (id_max >= u_info.ncolors):
            print('Number of panels exceeds max_number')


    ##
    ##
    ##
    def run( output_segment_info_db_file, id_tile_list, id_max, id_counts ):

        ## Write all segment info to a single file
        print 'Writing segmentInfo file (sqlite)'
        con = sqlite3.connect(output_segment_info_db_file)
        cur = con.cursor()

        cur.execute('DROP TABLE IF EXISTS idTileIndex;')
        cur.execute('CREATE TABLE idTileIndex (id int, w int, z int, y int, x int);')
        cur.execute('CREATE INDEX I_idTileIndex ON idTileIndex (id);')

        for entry_index in xrange(0, id_tile_list.shape[0]):
            cur.execute("INSERT INTO idTileIndex VALUES({0}, {1}, {2}, {3}, {4});".format( *id_tile_list[entry_index, :] ))

        #taken_names = {}
        cur.execute('DROP TABLE IF EXISTS segmentInfo;')
        cur.execute('CREATE TABLE segmentInfo (id int, name text, size int, confidence int);')
        cur.execute('CREATE UNIQUE INDEX I_segmentInfo ON segmentInfo (id);')

        for segment_index in xrange( 1, id_max + 1 ):
            if len( id_counts ) > segment_index and id_counts[ segment_index ] > 0:
                if segment_index == 0:
                    new_name = '__boundary__'
                else:
                    new_name = "segment{0}".format( segment_index )
                cur.execute('INSERT INTO segmentInfo VALUES({0}, "{1}", {2}, {3});'.format( segment_index, new_name, id_counts[ segment_index ], 0 ))
        con.commit()
        con.close()

##
##
    def backup( UserInfo, mojo_segment_info_db_backup_file ):
        con = sqlite3.connect( UserInfo.mojo_segment_info_db_file )
        cur = con.cursor()
        cur.execute( 'select * from idTileIndex;' )
        dbdata1 = cur.fetchall()
        cur.execute( 'select * from segmentInfo;' )
        dbdata2 = cur.fetchall()
        con.close()
        with open( mojo_segment_info_db_backup_file , 'wb') as f:
            pickle.dump([dbdata1, dbdata2], f)

##
    def restore( UserInfo, mojo_segment_info_db_backup_file ):

        with open( mojo_segment_info_db_backup_file , 'r') as f:
            [dbdata1, dbdata2] = pickle.load(f)

        con = sqlite3.connect( UserInfo.mojo_segment_info_db_file )
        cur = con.cursor()

        cur.execute('DROP TABLE IF EXISTS idTileIndex;')
        cur.execute('CREATE TABLE idTileIndex (id int, w int, z int, y int, x int);')
        cur.execute('CREATE INDEX I_idTileIndex ON idTileIndex (id);')
        for entry_index in xrange( len( dbdata1 ) ):
            cur.execute("INSERT INTO idTileIndex VALUES(?, ?, ?, ?, ?);", dbdata1[entry_index]  )


        initial_or_saved = len(dbdata2[0])
        cur.execute('DROP TABLE IF EXISTS segmentInfo;')
        if initial_or_saved == 4:
            cur.execute('CREATE TABLE segmentInfo (id int, name text, size int, confidence int);')
        elif initial_or_saved == 6:
            cur.execute('CREATE TABLE segmentInfo (id int, name text, size int, confidence int, type text, subtype text);')

        cur.execute('CREATE UNIQUE INDEX I_segmentInfo ON segmentInfo (id);')
        for entry_index in xrange( len( dbdata2 ) ):
            if initial_or_saved == 4:
                cur.execute("INSERT INTO segmentInfo VALUES(?, ?, ?, ?);", dbdata2[entry_index]  )
            elif initial_or_saved == 6:
                cur.execute("INSERT INTO segmentInfo VALUES(?, ?, ?, ?, ?, ?);", dbdata2[entry_index])


        con.commit()
        con.close()


